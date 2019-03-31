def make_pbfile(vis, pbfile):
    # from taskinit import im, ms, ia, qa, tb
    import numpy as np
    from scipy.constants import c

    ms.open(vis)
    fields = ms.range('field_id')['field_id']
    ms.done()
    im.open(vis)
    im.selectvis(field=fields[0])
    ms.open(vis)
    freq = np.mean(ms.range('chan_freq')['chan_freq'])
    phase_dir = ms.range('phase_dir')['phase_dir']['direction']
    ms.done()

    phase_dir = phase_dir[0][0], phase_dir[1][0]
    phase_dir = [qa.formxxx(str(phase_dir[0])+'rad', format='hms'),
                 qa.formxxx(str(phase_dir[1])+'rad', format='dms')]
    phase_dir = 'J2000 '+' '.join(phase_dir)

    tb.open(vis+'/ANTENNA/')
    dishdia = np.min(tb.getcol('DISH_DIAMETER'))
    tb.done()

    # pb of 512 pix cover pb down to 0.001
    # ensure largest pixel to pixel var to .01
    minpb = 0.001
    nx = 512
    cellconv = (nx*np.sqrt(np.log(2)/np.log(1/minpb)))**-1

    beam = c/freq/dishdia
    cell = {}
    cell['value'] = beam*cellconv
    cell['unit'] = 'rad'

#     nx = int(3*3e8/freq/dishdia*1.22*180/
#              math.pi*3600/qa.convert(advise['cell'],
#              'arcsec')['value'])
    # Chosen as to be 3 times fwhm of primary beam,
    # should include up to approximately .01 of peak flux

    im.defineimage(nx=nx, ny=nx, cellx=cell, celly=cell, phasecenter=phase_dir)
    im.setvp(dovp=True)
    im.makeimage(type='pb', image=pbfile)
    im.done()
    ia.open(pbfile)
    cs = ia.coordsys()
    cs.setreferencevalue(type='direction', value=[0., 0.])
    ia.setcoordsys(cs.torecord())
    ia.maskhandler('delete', 'mask0')
    ia.done()


make_pbfile('testdata.ms', 'VLA-1.4GHz.pb')