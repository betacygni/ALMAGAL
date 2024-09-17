import findContinuumCycle8 as fc

# Determine the rms of the final image
# This value is read in from the weblog
# For sources where the information is not stored in the weblog
# (due to bus in the pipeline tasks), we read the rms value using
# the imstat function within CASA
#
my_rms = []
for inloop in [0, 1, 2, 3]:
    if inloop in cubeInfo[1]:
        my_index = [index for index, item in enumerate(cubeInfo[1]) if item == inloop]
        my_rms.append(float(cubeInfo[8][my_index[0]].split()[0]))
    else:
        current_cube = cubes[inloop]
        current_rms = 1000.
        current_rms = min(current_rms, imstat(current_cube, chans='1100~1200')['rms'][0])
        current_rms = min(current_rms, imstat(current_cube, chans='1500~1600')['rms'][0])
        current_rms = min(current_rms, imstat(current_cube, chans='2000~2100')['rms'][0])
        current_rms = min(current_rms, imstat(current_cube, chans='3100~3200')['rms'][0])
        my_rms.append(current_rms)

# Main body of the REFIND.py script
# Written by Crystal Brogan and Todd Hunter
#
for spw in [0, 1, 2, 3]:
    cube = cubes[spw]
    rms = my_rms[spw]
    #rms = float(cubeInfo[8][spw].split()[0])
    os.system('rm -rf '+os.path.basename(cube)+'.*.*.mom8_fc*')
    os.system('rm -rf '+os.path.basename(cube)+'*.png')
    os.system('rm -rf '+os.path.basename(cube)+'.mom*.mask*')
    os.system('rm -rf '+os.path.basename(cube)+'*oint*')
    casalog.post("START REFIND")
    fcout=fc.findContinuum(cube,outdir='./',returnSigmaFindContinuum=True,mom0minsnr=5,mom8minsnr=mom8minsnrmask,
                           enableRejectNarrowInnerWindows=False)
    mom=os.path.basename(cube)+'.%.3f.mom8_fc'%(fcout[3])
    immoments(imagename=cube,moments=[8],chans=fcout[0],outfile=mom)
    stats=imstat(mom)
    peaksig=stats['max'][0]/rms
    npix=imstat(mom,mask='"'+mom+'"'+'>'+str(peaksigCut*rms))['npts']
    if len(npix) > 0:
        npix = npix[0]
    else:
        npix = 0
    casalog.post("REFIND One 10: %s, %.3f, %.3f, %d, BW %.3f, %s"%(mom,stats['max'][0],peaksig,npix,fcout[2],fcout[0]))
    # Insert 6 here
    iteration = 1
    newfc = fcout[3]*0.9 # lower the starting point
    while peaksig > peaksigCut and npix > npixCut and iteration < 6: 
        if iteration == 3: 
            if os.path.exists(os.path.basename(cube)+'.joint.mask2'):
                currentmask=os.path.basename(cube)+'.joint.mask2'
            else:
                currentmask=os.path.basename(cube)+'.joint.mask'
            outstatsPeak=imstat(mom,mask='"'+currentmask+'"<1')
            if len(outstatsPeak['max']) > 0:
                outpeaksig=outstatsPeak['max'][0]/rms 
            else:
                outpeaksig = 0             
            if outpeaksig > peaksigCut:
                newfc = fcout[3] * 0.995 # since mask will change don't want a big jump, but avoid same name as previous iteration.
                casalog.post("In REFIND Amending mask in iteration 4")
                os.system('rm -rf '+currentmask+'.amended')
                immath(imagename=[currentmask,mom],outfile=currentmask+'.amended',mode='evalexpr',
                       expr='iif((IM0==1)||(IM1>%f), 1, 0)'%(peaksigCut*rms))
                fcout=fc.findContinuum(cube,outdir='./',sigmaFindContinuum=newfc,returnSigmaFindContinuum=True,
                                       userJointMask=currentmask+'.amended',
                                       narrow=2,enableRejectNarrowInnerWindows=False)
                os.rename(os.path.basename(cube)+'.meanSpectrum.userJointMask',os.path.basename(cube)+'.meanSpectrum.mom0mom8jointMask')
            else:
                fcout=fc.findContinuum(cube,outdir='./',sigmaFindContinuum=newfc,returnSigmaFindContinuum=True,
                                       meanSpectrumFile=os.path.basename(cube)+'.meanSpectrum.mom0mom8jointMask',
                                       narrow=2,enableRejectNarrowInnerWindows=False)               
        else:
            fcout=fc.findContinuum(cube,outdir='./',sigmaFindContinuum=newfc,returnSigmaFindContinuum=True,
                                   meanSpectrumFile=os.path.basename(cube)+'.meanSpectrum.mom0mom8jointMask',
                                   narrow=2,enableRejectNarrowInnerWindows=False)  
        mom=os.path.basename(cube)+'.%.3f.mom8_fc'%(fcout[3])        
        immoments(imagename=cube,moments=[8],chans=fcout[0],outfile=mom)
        stats=imstat(mom)
        peaksig=stats['max'][0]/rms
        npix=imstat(mom,mask='"'+mom+'"'+'>'+str(peaksigCut*rms))['npts']
        if len(npix) > 0:
            npix = npix[0]
        else:
            npix = 0
        casalog.post("REFIND: %s, %d, %.3f, %.3f, %d, BW %.3f, %s"%(mom,iteration,stats['max'][0],peaksig,npix,fcout[2],fcout[0]))
        iteration = iteration + 1
        newfc = fcout[3]*0.95
    if peaksig > peaksigCut and npix > npixCut:  # iteration = 6
        cubestats=imstat(cube,chans=fcout[0],axes=[0,1,2],mask='"'+cube+'">%f'%(peaksigCut*rms))
        keepchans=np.where(cubestats['npts']==0)
        badchans=np.where(cubestats['npts']>0)
        keeprange=au.channelSelectionRangesToIndexArray(fcout[0])[keepchans]
        badrange=au.channelSelectionRangesToIndexArray(fcout[0])[badchans]
        badstr=au.channelSelectionArrayToRangeString(badrange)               
        fcout=fc.findContinuum(cube,outdir='./',sigmaFindContinuum=fcout[3],returnSigmaFindContinuum=True,
                               meanSpectrumFile=os.path.basename(cube)+'.meanSpectrum.mom0mom8jointMask',
                               narrow=2,enableRejectNarrowInnerWindows=False,
                               png=os.path.basename(cube)+'meanSpectrum.mom0mom8jointMask.min.min.'+str(fcout[3])+'sigma.narrow2.trimauto_max=20.new.png',
                               avoidance=badstr)      
        mom=os.path.basename(cube)+'.%.3f.mom8_fc'%(fcout[3])        
        immoments(imagename=cube,moments=[8],chans=fcout[0],outfile=mom+'.new')
        stats=imstat(mom+'.new')
        peaksig=stats['max'][0]/rms
        npix=imstat(mom,mask='"'+mom+'.new'+'"'+'>'+str(peaksigCut*rms))['npts']
        if len(npix) > 0:
            npix = npix[0]
        else:
            npix = 0
        casalog.post("REFIND: %s, %d, %.3f, %.3f, %d, BW %.3f, %s"%(mom+'.new',iteration,stats['max'][0],peaksig,npix,fcout[2],fcout[0]))
