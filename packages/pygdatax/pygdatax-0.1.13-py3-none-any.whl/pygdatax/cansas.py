import nexusformat.nexus as nx
import fabio


def createEmptyNXsas(filenanme, detector_number=1, instrument_name='genericSAS'):
    root = nx.NXroot()
    root.attrs['default'] = 'entry'
    root.attrs['NX_class'] = b'NXroot'
    entry = nx.NXentry()
    entry.attrs['default'] = 'data'
    entry.attrs['version'] = '1.1'
    entry.title = nx.NXfield(value='')
    entry.run = nx.NXfield(value='')
    entry.definition = nx.NXfield(definition='NXpygdatax')
    # entry.date=nx.NXfield(date=)
    # building instrument
    instrument = nx.NXinstrument(description=instrument_name)
    # intrument/aperture
    aperture = nx.NXslit(x_gap=nx.NXfield(0, attrs={'units': 'mm'}),
                         y_gap=nx.NXfield(0, attrs={'units': 'mm'}))
    # TO DO : find good distance
    collimator = nx.NXcollimator(length=nx.NXfield(1200, units='mm'),
                                 distance=nx.NXfield(200, units='mm'))
    # instrument/detector
    dist = float(header['SampleDistance']) * 1000
    detx = float(header['detx'])
    detz = float(header['detz'])
    pixSize1 = float(header['PSize_1']) * 1000
    pixSize2 = float(header['PSize_2']) * 1000
    x0 = float(header['Center_1'])
    y0 = float(header['Center_2'])
    detector = nx.NXdetector(data=fileObj.data,
                             distance=nx.NXfield(dist, attrs={'units': 'mm'}),
                             x_position=nx.NXfield(detx, attrs={'units': 'mm'}),
                             y_position=nx.NXfield(detz, attrs={'units': 'mm'}),
                             beam_center_x=nx.NXfield(x0, attrs={'units': 'pixel'}),
                             beam_center_y=nx.NXfield(y0, attrs={'units': 'pixel'}),
                             x_pixel_size=nx.NXfield(pixSize1, attrs={'units': 'mm'}),
                             y_pixel_size=nx.NXfield(pixSize2, attrs={'units': 'mm'}),
                             description='Pilatus 1M',
                             pixel_mask_applied=False,
                             pixel_mask = np.zeros_like(fileObj.data)
                             )
    # instrument/source
    wvl = float(header['WaveLength']) * 1e10
    sizeX = float(header['s1hr']) + float(header['s1hl'])
    sizeY = float(header['s1bot']) + float(header['s1top'])
    source = nx.NXsource(description='genix3D', radiation='x-ray',
                         incident_wavelength=nx.NXfield(wvl, attrs={'units': 'angstrom'}),
                         incident_wavelength_spread=0,
                         beam_size_x=nx.NXfield(sizeX, attrs={'units': 'mm'}),
                         beam_size_y=nx.NXfield(sizeY, attrs={'units': 'mm'}),
                         flux=nx.NXfield(float(header['pilai1']), attrs={'units': '1/s'}))
    entry.instrument = instrument
    entry.instrument.insert(detector)
    entry.instrument.insert(aperture)
    entry.instrument.insert(collimator)
    entry.instrument.insert(source)

    sample = nx.NXsample(sample_name=header['Comment'],
                         thickness=nx.NXfield(1.0, attrs={'units': 'mm'}),
                         transmission=float(header['pilroi1']),
                         x_position=nx.NXfield(float(header['x']), attrs={'units': 'mm'}),
                         y_position=nx.NXfield(float(header['z']), attrs={'units': 'mm'}),
                         om=nx.NXfield(float(header['om']), attrs={'units': 'deg'}),
                         phi=nx.NXfield(float(header['phi']), attrs={'units': 'deg'}),
                         rx=nx.NXfield(float(header['rx']), attrs={'units': 'deg'}),
                         ry=nx.NXfield(float(header['ry']), attrs={'units': 'deg'}),
                         temperature=nx.NXfield(float(header['Temperature']),
                                                attrs={'units': '°C'}),
                         count_time=nx.NXfield(float(header['count_time']),
                                               attrs={'units': 's'}),
                         description=header['Comment']
                         )
    entry.insert(sample)
    entry.data = nx.NXdata(attrs={'interpretation': b"image",
                                  'signal': "data"})
    root.entry0 = entry
    root.entry0.data.makelink(root.entry0.instrument.detector.data)
    new_name = filename.split('.')[0]
    new_name += '.nxs'
    try:
        root.save(new_name, mode='w')
        root.close()
    except NeXusError:
        print('error')
        # if os.path.exists(new_name):
        #     print('already here')
        #     os.remove(new_name)
        #     root.save(new_name, mode='w')
        #     root.unlock()
        # else:
        #     print('something else')

    return root

def sansllb2nxcansas(nexusfile):
    pass

def build_nexus_from_edf(filename):
    fileObj = fabio.open(filename)
    header = fileObj.header
    root = nx.NXroot()
    root.attrs['default'] = 'entry'
    root.attrs['NX_class'] = b'NXroot'

    entry = nx.NXentry()
    entry.attrs['default'] = 'data'
    entry.attrs['canSAS_class'] = 'SASentry'
    entry.attrs['version'] = '1.0'
    entry.definition = nx.NXfield(definition='NXcanSAS')
    entry.title = nx.NXfield(value=header['title'])
    entry.run = nx.NXfield(value=header['run'])

    # entry.date=nx.NXfield(date=)
    # building instrument
    instrument = nx.NXinstrument(description='Xeuss')
    y_gap = float(header['s2bot']) + float(header['s2top'])
    x_gap = float(header['s2hr']) + float(header['s2hl'])
    # intrument/aperture
    aperture = nx.NXslit(x_gap=nx.NXfield(x_gap, attrs={'units': 'mm'}),
                         y_gap=nx.NXfield(y_gap, attrs={'units': 'mm'}))
    # TO DO : find good distance
    collimator = nx.NXcollimator(length=nx.NXfield(1200, units='mm'),
                                 distance=nx.NXfield(200, units='mm'),
                                 s1bot=nx.NXfield(float(header['s1bot']), attrs={'units': 'mm'}),
                                 s1top=nx.NXfield(float(header['s1top']), attrs={'units': 'mm'}),
                                 s1hl=nx.NXfield(float(header['s1hl']), attrs={'units': 'mm'}),
                                 s1hr=nx.NXfield(float(header['s1hr']), attrs={'units': 'mm'}),
                                 s2bot=nx.NXfield(float(header['s1bot']), attrs={'units': 'mm'}),
                                 s2top=nx.NXfield(float(header['s1top']), attrs={'units': 'mm'}),
                                 s2hl=nx.NXfield(float(header['s2hl']), attrs={'units': 'mm'}),
                                 s2hr=nx.NXfield(float(header['s2hr']), attrs={'units': 'mm'}))
    # instrument/detector
    dist = float(header['SampleDistance']) * 1000
    detx = float(header['detx'])
    detz = float(header['detz'])
    pixSize1 = float(header['PSize_1']) * 1000
    pixSize2 = float(header['PSize_2']) * 1000
    x0 = float(header['Center_1'])
    y0 = float(header['Center_2'])
    detector = nx.NXdetector(data=fileObj.data,
                             distance=nx.NXfield(dist, attrs={'units': 'mm'}),
                             x_position=nx.NXfield(detx, attrs={'units': 'mm'}),
                             y_position=nx.NXfield(detz, attrs={'units': 'mm'}),
                             beam_center_x=nx.NXfield(x0, attrs={'units': 'pixel'}),
                             beam_center_y=nx.NXfield(y0, attrs={'units': 'pixel'}),
                             x_pixel_size=nx.NXfield(pixSize1, attrs={'units': 'mm'}),
                             y_pixel_size=nx.NXfield(pixSize2, attrs={'units': 'mm'}),
                             description='Pilatus 1M',
                             pixel_mask_applied=False,
                             pixel_mask=np.zeros_like(fileObj.data))
    # instrument/source
    wvl = float(header['WaveLength']) * 1e10
    sizeX = float(header['s1hr']) + float(header['s1hl'])
    sizeY = float(header['s1bot']) + float(header['s1top'])
    source = nx.NXsource(description='genix3D', radiation='x-ray',
                         incident_wavelength=nx.NXfield(wvl, attrs={'units': 'angstrom'}),
                         incident_wavelength_spread=0,
                         beam_size_x=nx.NXfield(sizeX, attrs={'units': 'mm'}),
                         beam_size_y=nx.NXfield(sizeY, attrs={'units': 'mm'}),
                         flux=nx.NXfield(float(header['pilai1']), attrs={'units': '1/s'}))
    entry.instrument = instrument
    entry.instrument.insert(detector)
    entry.instrument.insert(aperture)
    entry.instrument.insert(collimator)
    entry.instrument.insert(source)

    sample = nx.NXsample(sample_name=header['Comment'],
                         thickness=nx.NXfield(1.0, attrs={'units': 'mm'}),
                         transmission=float(header['pilroi1']),
                         x_position=nx.NXfield(float(header['x']), attrs={'units': 'mm'}),
                         y_position=nx.NXfield(float(header['z']), attrs={'units': 'mm'}),
                         om=nx.NXfield(float(header['om']), attrs={'units': 'deg'}),
                         phi=nx.NXfield(float(header['phi']), attrs={'units': 'deg'}),
                         rx=nx.NXfield(float(header['rx']), attrs={'units': 'deg'}),
                         ry=nx.NXfield(float(header['ry']), attrs={'units': 'deg'}),
                         temperature=nx.NXfield(float(header['Temperature']),
                                                attrs={'units': '°C'}),
                         count_time=nx.NXfield(float(header['count_time']),
                                               attrs={'units': 's'}),
                         description=header['Comment']
                         )
    entry.insert(sample)
    entry.data = nx.NXdata(attrs={'interpretation': b"image",
                                  'signal': "data"})
    root.entry0 = entry
    root.entry0.data.makelink(root.entry0.instrument.detector.data)
    new_name = filename.split('.')[0]
    new_name += '.nxs'
    try:
        root.save(new_name, mode='w')
        root.close()
    except NeXusError:
        print('error')
        # if os.path.exists(new_name):
        #     print('already here')
        #     os.remove(new_name)
        #     root.save(new_name, mode='w')
        #     root.unlock()
        # else:
        #     print('something else')

    return root
