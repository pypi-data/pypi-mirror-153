import os
import io
import sys
import csv
import math
import glob
import shutil

import numpy as np
import django
from django.db import models
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

import astropy.units as u
from astropy.table import Table
from astropy.io.votable import from_table, writeto
from astropy.io.votable.tree import Param
from astropy.io import fits
from astropy.wcs import WCS
from astropy.visualization import PercentileInterval
from astroquery.skyview import SkyView
from astropy.utils.data import clear_download_cache


Run, Instance, Detection, Product, Source  = None, None, None, None, None
SourceDetection, Comment, Tag, TagSourceDetection = None, None, None, None


# utils
def _write_bytesio_to_file(filename, bytesio):
    """Write the contents of the given BytesIO to a file.
    Creates the file or overwrites the file if it does
    not exist yet. 
    
    """
    with open(filename, "wb") as outfile:
        # Copy the BytesIO stream to the output file
        outfile.write(bytesio.getbuffer())
            

def _write_zipped_fits_file(filename, product, compress=True):
    """Compress a .fits file as .fits.gz for a data product.
   
    """
    with io.BytesIO() as buf:
        buf.write(product)
        buf.seek(0)
        if not os.path.isfile(filename):
            _write_bytesio_to_file(filename, buf)
            if compress:
                os.system(f'gzip {filename}')


def _write_products(products, prefix):
    _write_zipped_fits_file('%s_cube.fits' % (prefix), products.cube)
    _write_zipped_fits_file('%s_chan.fits' % (prefix), products.chan)
    _write_zipped_fits_file('%s_mask.fits' % (prefix), products.mask)
    _write_zipped_fits_file('%s_mom0.fits' % (prefix), products.mom0)
    _write_zipped_fits_file('%s_mom1.fits' % (prefix), products.mom1)
    _write_zipped_fits_file('%s_mom2.fits' % (prefix), products.mom2)

    # Open spectrum
    with io.BytesIO() as buf:
        buf.write(b''.join(products.spec))
        buf.seek(0)
        spec_file  = '%s_spec.txt' % (prefix)
        if not os.path.isfile(spec_file):
            _write_bytesio_to_file(spec_file, buf)


# Connect to WALLABY database
def connect():
    global Run, Instance, Detection, Product, Source
    global SourceDetection, Comment, Tag, TagSourceDetection
    os.environ["DJANGO_SECRET_KEY"] = "-=(gyah-@e$-ymbz02mhwu6461zv&1&8uojya413ylk!#bwa-l"
    os.environ["DJANGO_SETTINGS_MODULE"] = "api.settings"
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "True"
    os.environ["DATABASE_HOST"] = "146.118.67.204"
    os.environ["DATABASE_NAME"] = "wallabydb"
    os.environ["DATABASE_USER"] = "wallaby_user"
    os.environ["DATABASE_PASSWORD"] = "LKaRsQrNtXZ7vN8L*6"
    sys.path.append("/mnt/shared/wallaby/apps/SoFiAX_services/api/")
    django.setup()
    from tables.models import Run, Instance, Detection, Product, Source
    from tables.models import SourceDetection, Comment, Tag, TagSourceDetection
    return


# TODO(austin): get multiple catalogues by tags


# Retrieve catalogue by tag
def get_catalog(tag):
    tag = str(tag)
    if tag == "":
        sys.stderr.write("Please specify a tag to extract a source catalogue, e.g.:\ntable = get_catalog(tag=\"NGC 5044 DR1\")\n")
        return None
    
    table = Table()
    
    # Get field names
    detection_field_names = [field.name for field in Detection._meta.fields if not isinstance(field, models.ForeignKey)]
    detection_field_names.remove("name")
    detection_field_names.remove("unresolved")
    detection_field_names.remove("v_opt")
    detection_field_names.remove("v_app")
    detection_field_names.remove("v_rad")
    detection_field_names.remove("l")
    detection_field_names.remove("b")
    detection_field_names.remove("wm50")
    detection_field_names.remove("v_opt_peak")
    detection_field_names.remove("v_app_peak")
    detection_field_names.remove("v_rad_peak")
    detection_field_names.remove("l_peak")
    detection_field_names.remove("b_peak")
    detection_field_names.remove("x_peak")
    detection_field_names.remove("y_peak")
    detection_field_names.remove("z_peak")
    detection_field_names.remove("ra_peak")
    detection_field_names.remove("dec_peak")
    detection_field_names.remove("freq_peak")
    source_field_names = [field.name for field in Source._meta.fields if not isinstance(field, models.ForeignKey)]
    source_field_names.remove("id")
    
    # Get sources and detections
    sources = [
        Source.objects.get(id=sd.source_id) for sd in [
            SourceDetection.objects.get(id=tsd.source_detection_id) for tsd in 
                TagSourceDetection.objects.filter(tag_id=Tag.objects.get(name=tag).id)
        ]
    ]
    detections = [
        Detection.objects.get(id=sd.detection_id) for sd in [
            SourceDetection.objects.get(id=tsd.source_detection_id) for tsd in 
                TagSourceDetection.objects.filter(tag_id=Tag.objects.get(name=tag).id)
        ]
    ]
    
    # Add columns to the table
    for field in source_field_names:
        if field == 'name':
            table[field] = [getattr(s, field) for s in sources]
        else:
            table[field] = np.array([getattr(s, field) for s in sources], dtype=float)
    for field in detection_field_names:
        table[field] = np.array([getattr(d, field) for d in detections], dtype=float)
    
    # Extract and add comments, if any
    column_comments = []
    for i in range(len(table)):
        column_comments.append([])
        comments = Comment.objects.filter(detection=table["id"][i])
        for comment in comments:
            column_comments[i].append(comment.comment + " (" + comment.author + ")")
    table.add_column(col=column_comments, name="comments")
    
    # Extract and add tags, if any
    column_tags = []
    for i in range(len(table)):
        column_tags.append([])
        tags = TagSourceDetection.objects.filter(source_detection_id=SourceDetection.objects.get(detection_id=table["id"][i]))
        for t in tags:
            column_tags[i].append(Tag.objects.get(id=t.tag_id).name)
    table.add_column(col=column_tags, name="tags")

    # Extract team release column
    team_release = tag.replace('DR', 'TR')
    column_team_release = [str(team_release)] * len(table)
    table.add_column(col=column_team_release, name='team_release')

    # Add additional properties
    c = 299792.458
    H0 = 70
    f0 = 1.420405751768E9
    dist_h = c * ((f0 / table['freq']) - 1.0) / H0
    HI_mass = np.log10(49.7 * dist_h ** 2 * table['f_sum'])
    table.add_column(col=dist_h, name='dist_h')
    table.add_column(col=HI_mass, name='log_m_hi')

    return table


def save_catalog(tag, *args, **kwargs):
    """Write catalog of tagged sources. Remove object columns for write to file.

    """
    table = get_catalog(tag)
    table.remove_columns(['tags'])
    table.write(*args, **kwargs)


def save_products_for_source(tag, source_name, *args, **kwargs):
    """Save source finding output products for a given source name.

    """
    table = get_catalog(tag)
    try:
        idx = list(table['name']).index(source_name)
        row = table[idx]
    except Exception as e:
        sys.stderr.write("Could not find source with provided name in tagged data.")
        return None
    detection = Detection.objects.get(id=row['id'])
    products = Product.objects.get(detection=detection)

    name = source_name.replace(' ', '_')
    parent = f'{name}_products'
    if not os.path.isdir(parent):
        os.mkdir(parent)
    
    # Write fits files
    _write_products(products, f'{parent}/{name}')
    
    return


def save_products(tag, *args, **kwargs):
    """Save source finding output products for a given tag

    """
    table = get_catalog(tag)
    parent = '%s_products' % tag.replace(' ', '_')
    if not os.path.isdir(parent):
        os.mkdir(parent)

    for row in table:
        name = row['name'].replace(' ', '_')
        if not os.path.isdir(f'{parent}/{name}'):
            os.mkdir(f'{parent}/{name}')
        detection = Detection.objects.get(id=row['id'])
        products = Product.objects.get(detection=detection)
        _write_products(products, f'{parent}/{name}/{name}')

    os.system(f'tar -czf {parent}.tar.gz {parent}')

    return


# Print list of supported tags
def print_tags():
    tags = Tag.objects.all()
    for tag in tags:
        print("{:20s}\t{:s}".format("\"" + tag.name + "\"", tag.description))
    return


# Retrieve FITS image from database
def get_image(product):
    with io.BytesIO() as buf:
        buf.write(product)
        buf.seek(0)
        hdu = fits.open(buf)[0]
        return hdu.data, hdu.header


# Retrieve spectrum from database
def get_spectrum(product):
    with io.BytesIO() as buf:
        buf.write(b"".join(product))
        buf.seek(0)
        return np.loadtxt(buf, dtype="float", comments="#", unpack=True)


# Retrieve DSS image from Skyview
def retrieve_dss_image(longitude, latitude, width, height):
    hdulist = SkyView.get_images(
        position="{}, {}".format(longitude, latitude),
        survey=["DSS"],
        coordinates="J2000",
        projection="Tan",
        width=width*u.deg,
        height=height*u.deg,
        cache=None
    )
    return hdulist[0][0]


# Create overview plot
def overview_plot(id):
    interval = PercentileInterval(95.0)
    plt.rcParams["figure.figsize"] = (16, 12)
    fig = plt.figure()
    
    # Retrieve products from database
    products = Product.objects.get(detection=id)
    
    # Open moment 0 image
    mom0, header = get_image(products.mom0)
    mom1, header = get_image(products.mom1)
    spectrum = get_spectrum(products.spec)
    wcs = WCS(header)
    
    # Extract coordinate information
    nx = header["NAXIS1"]
    ny = header["NAXIS2"]
    lon, lat = wcs.all_pix2world(nx/2, ny/2, 0)
    tmp1, tmp3 = wcs.all_pix2world(0, ny/2, 0)
    tmp2, tmp4 = wcs.all_pix2world(nx, ny/2, 0)
    width = np.rad2deg(math.acos(math.sin(np.deg2rad(tmp3)) * math.sin(np.deg2rad(tmp4)) + math.cos(np.deg2rad(tmp3)) * math.cos(np.deg2rad(tmp4)) * math.cos(np.deg2rad(tmp1 - tmp2))))
    tmp1, tmp3 = wcs.all_pix2world(nx/2, 0, 0)
    tmp2, tmp4 = wcs.all_pix2world(nx/2, ny, 0)
    height = np.rad2deg(math.acos(math.sin(np.deg2rad(tmp3)) * math.sin(np.deg2rad(tmp4)) + math.cos(np.deg2rad(tmp3)) * math.cos(np.deg2rad(tmp4)) * math.cos(np.deg2rad(tmp1 - tmp2))))
    
    # Plot DSS image with HI contours
    try:
        hdu_opt = retrieve_dss_image(lon, lat, width, height)
        wcs_opt = WCS(hdu_opt.header)
        
        bmin, bmax = interval.get_limits(hdu_opt.data)
        ax = plt.subplot(2, 2, 2, projection=wcs_opt)
        ax.imshow(hdu_opt.data, origin="lower")
        ax.contour(mom0, transform=ax.get_transform(wcs), levels=np.logspace(2.0, 5.0, 10), colors="lightgrey", alpha=1.0)
        ax.grid(color="grey", ls="solid")
        ax.set_xlabel("Right ascension (J2000)")
        ax.set_ylabel("Declination (J2000)")
        ax.tick_params(axis="x", which="both", left=False, right=False)
        ax.tick_params(axis="y", which="both", top=False, bottom=False)
        ax.set_title("DSS + Moment 0")
        ax.set_aspect(np.abs(wcs_opt.wcs.cdelt[1] / wcs_opt.wcs.cdelt[0]))
    except:
        sys.stderr.write("Failed to retrieve DSS image.\n")
        pass
    
    # Plot moment 0
    ax2 = plt.subplot(2, 2, 1, projection=wcs)
    ax2.imshow(mom0, origin="lower")
    ax2.grid(color="grey", ls="solid")
    ax2.set_xlabel("Right ascension (J2000)")
    ax2.set_ylabel("Declination (J2000)")
    ax2.tick_params(axis="x", which="both", left=False, right=False)
    ax2.tick_params(axis="y", which="both", top=False, bottom=False)
    ax2.set_title("Moment 0")
    
    # Add beam size
    ax2.add_patch(Ellipse((5, 5), 5, 5, 0, edgecolor="grey", facecolor="grey"))

    # Plot moment 1
    bmin, bmax = interval.get_limits(mom1)
    ax3 = plt.subplot(2, 2, 3, projection=wcs)
    ax3.imshow(mom1, origin="lower", vmin=bmin, vmax=bmax, cmap=plt.get_cmap("gist_rainbow"))
    ax3.grid(color="grey", ls="solid")
    ax3.set_xlabel("Right ascension (J2000)")
    ax3.set_ylabel("Declination (J2000)")
    ax3.tick_params(axis="x", which="both", left=False, right=False)
    ax3.tick_params(axis="y", which="both", top=False, bottom=False)
    ax3.set_title("Moment 1")
    
    # Plot spectrum
    xaxis = spectrum[1] / 1e+6
    data  = 1000.0 * np.nan_to_num(spectrum[2])
    xmin = np.nanmin(xaxis)
    xmax = np.nanmax(xaxis)
    ymin = np.nanmin(data)
    ymax = np.nanmax(data)
    ymin -= 0.1 * (ymax - ymin)
    ymax += 0.1 * (ymax - ymin)
    ax4 = plt.subplot(2, 2, 4)
    ax4.step(xaxis, data, where="mid", color="royalblue")
    ax4.set_xlabel("Frequency (MHz)")
    ax4.set_ylabel("Flux density (mJy)")
    ax4.set_title("Spectrum")
    ax4.grid(True)
    ax4.set_xlim([xmin, xmax])
    ax4.set_ylim([ymin, ymax])
    
    fig.canvas.draw()
    plt.tight_layout()
    
    return plt


def save_overview(tag, *args, **kwargs):
    """Save overview plots for tagged sources

    """
    table = get_catalog(tag)
    parent = '%s_overview' % tag.replace(' ', '_')
    if not os.path.isdir(parent):
        os.mkdir(parent)    

    for row in table:
        name = row['name'].replace(' ', '_')
        p = overview_plot(row['id'])
        p.savefig(f"{parent}/{name}_overview.png")
        p.close()

    os.system(f'tar -czf {parent}.tar.gz {parent}')

    return


def save_spectrum(detection, filename):
    products = Product.objects.get(detection=detection)
    spectrum = products.spec
    
    # store spectrum as numpy array     
    array = []
    with io.BytesIO() as buf:
        buf.write(b''.join(products.spec))
        buf.seek(0)
        text = buf.getbuffer().tobytes().decode('utf-8')
        lines = text.strip().split('\n')
        for line in lines:
            if not line.startswith('#'):
                chan, freq, flux, pix = line.strip().split()
                array.append(np.array([int(chan), float(freq), float(flux), int(pix)]))
    array = np.array(array)
    
    # write to fits file
    t = Table(array, names=('Channel', 'Frequency', 'Flux Density', 'Pixels'), dtype=(int, np.float32, np.float32, int))
    t.write(filename, format='fits')
    
    # update spectrum metadata
    spectrum = fits.open(filename, 'update')
    spectrum[0].data = np.array([[[0]]]).astype('int16')
    hdr = spectrum[0].header
    hdr['WCSAXES'] = 3
    hdr['CRPIX1'] = 0
    hdr['CRPIX2'] = 0
    hdr['CRPIX3'] = 0
    hdr['CDELT1'] = -0.00166666
    hdr['CDELT2'] = 0.00166666
    hdr['CDELT3'] = 18518.
    hdr['CUNIT1'] = 'deg'
    hdr['CUNIT2'] = 'deg'
    hdr['CUNIT3'] = 'Hz'
    hdr['CTYPE1'] = 'RA---SIN'
    hdr['CTYPE2'] = 'DEC--SIN'
    hdr['CTYPE3'] = 'FREQ'
    hdr['CRVAL1'] = detection.ra
    hdr['CRVAL2'] = detection.dec
    hdr['CRVAL3'] = detection.freq

    # Provenance metadata
    hdr['SBID'] = ''
    hdr['SRCVER'] = ''
    hdr['SRCTR'] = ''
    hdr['DATE'] = datetime.now().isoformat()

    spectrum.close()
    return


def casda_deposit(table, deposit_name):
    """Export source data products and catalogue for Astropy table for CASDA release.
    Will create an output directory with the deposit name and store products in that folder.

    """
    # ensure output directory exists
    if not os.path.exists(deposit_name):
        os.mkdir(deposit_name)
    else:
        raise Exception("Output directory exists but is not empty.")

    # subdirectories
    os.mkdir(f'{deposit_name}/catalogue')
    os.mkdir(f'{deposit_name}/cubelets')
    os.mkdir(f'{deposit_name}/spectra')
    os.mkdir(f'{deposit_name}/moment_maps')
    os.mkdir(f'{deposit_name}/plots')

    # Export products
    for row in table:
        name = row['name'].replace(' ', '_')
        release = row['team_release'].replace(' ', '_')
        detection = Detection.objects.get(id=row['id'])
        products = Product.objects.get(detection=detection)
        filename_prefix = f'{name}_{release}'
        
        # write .fits files
        _write_zipped_fits_file('%s/%s/%s_cube.fits' % (deposit_name, 'cubelets', filename_prefix), products.cube, compress=False)
        _write_zipped_fits_file('%s/%s/%s_chan.fits' % (deposit_name, 'moment_maps', filename_prefix), products.chan, compress=False)
        _write_zipped_fits_file('%s/%s/%s_mask.fits' % (deposit_name, 'cubelets', filename_prefix), products.mask, compress=False)
        _write_zipped_fits_file('%s/%s/%s_mom0.fits' % (deposit_name, 'moment_maps', filename_prefix), products.mom0, compress=False)
        _write_zipped_fits_file('%s/%s/%s_mom1.fits' % (deposit_name, 'moment_maps', filename_prefix), products.mom1, compress=False)
        _write_zipped_fits_file('%s/%s/%s_mom2.fits' % (deposit_name, 'moment_maps', filename_prefix), products.mom2, compress=False)
        save_spectrum(detection, '%s/%s/%s_spec.fits' % (deposit_name, 'spectra', filename_prefix))

        # add source name to each header file
        product_files = glob.glob(f'{deposit_name}/{name}_{release}*.fits')
        for f in product_files:
            hdul = fits.open(f, 'update')
            hdr = hdul[0].header
            hdr['WALTR'] = release
            hdul.close()

        # TODO: add SDIBs to WALSBID header cards 

        # TODO: add moment 0 maps (png) to products under separate folder
        mom0, _ = get_image(products.mom0)
        plt.imshow(mom0)
        plt.axis('off')
        plt.savefig('%s/%s/%s_mom0.png' % (deposit_name, 'plots', filename_prefix))
        plt.close()

    # Read columns and metadata
    table_columns = {}
    module_path = os.path.dirname(os.path.abspath(__file__))
    with open(f'{module_path}/source_column_metadata.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            name, ucd, units, description = row
            units = units.replace('pixel', 'pix')
            if units == '-':
                units = None
            table_columns[name] = (ucd, units, description)

    # Export catalogue
    column_names = [k for k in table_columns.keys()]
    table.remove_column('id')
    table.remove_column('tags')
    table = table[column_names]
    votable = from_table(table)
    votable.version = '1.3'

    # Update fields
    fields = []
    for name, meta in table_columns.items():
        ucd, units, description = meta
        field = votable.get_field_by_id(name)
        field.ucd = ucd
        field.unit = units
        field.description = description
        fields.append(field)
        if field.datatype == 'unicodeChar':
            field.datatype = 'char'

    for resource in votable.resources:        
        # update rows
        for t in resource.tables:
            for i, row in enumerate(fields):
                t.fields[i] = row

            # add params
            t.params.append(Param(votable, ID='catalogueName', name='Catalogue Name', value=deposit_name, arraysize='59'))
            t.params.append(Param(votable, ID='indexedFields', name='Indexed Fields', value='name,ra,dec,freq,f_sum,w20,team_release', arraysize='255'))
            t.params.append(Param(votable, ID='principalFields', name='Principal Fields', value='name,ra,dec,freq,f_sum,w20,team_release', arraysize='255'))

    catalogue_file = f'{deposit_name}/catalogue/catalogue.xml'
    writeto(votable, catalogue_file)

    return