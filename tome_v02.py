"""
Tome v02 A compilation of all Lars' python scripts as callable functions

functions:
    alpha (returns column index from numerical index for excel files)
    bindata (bins a list of values)
    binnspectra (bins n mass spectra together into a single mass spectrum)
    bincidspectra (bins mass spectra together based on their collision voltage)
    filepresent (checks for a file or directory in the current working directory)
    find_all (finds all locations of files of a given name in a provided directory)
    linmag (generates a list of values which is linear in magnification)
    linramp (generates a list of values which is linear from start to finish)
    lyround (rounds a number given a particular base number)
    mag (calculates and returns the magnification of a given y value relative to the start)
    msipoverlay (generates a figure overlaying predicted isotope patterns on top of experimental data)
    normalize (normalizes a list to a given value)
    resolution (calculates the resolution of a spectrum peak)
    sigmafwhm (cacluates sigma and fwhm from a resolution and a mass)
    strtolist (converts a string to a list)        

changelog:
    created mzML class and moved many functions to work within that class (removed several functions from Tome)
    added strtolist
    moved classes to separate files
    fullspeclist has been moved to _Spectrum class (there were issues with mutation of the original)
    calcindex has also been moved to _Spectrum class (it is used solely in that class)
    moved colours to _Colour class
    removed automz (now handled in the Molecule class)
    created bincidspectra to bin spectra with the same cid together
    removed loadwb, openpyxlcheck, pullparams (now included in XLSX class)
    generalized filepresent
    removed pwconvert (now included in mzML class)
    completely rewrote resolution
    ---v02---


"""
# ----------------------------------------------------------
# -------------------FUNCTION DEFINITIONS-------------------
# ----------------------------------------------------------

def alpha(index):
    """
    function for taking an index and converting it to the corresponding column used by excel
    works up to column ZY (column # 701)
    """
    import string
    alphabet = list(string.ascii_lowercase)
    out = ''
    n = (index+1)/26
    if n != 0:
        out += alphabet[n-1]
        out += alphabet[(index+1)%26-1]
    else:
        out = alphabet[index]
    return out.upper()

def bindata(n,v,lst):
    """
    Function for summing a supplied list of data (binning)
    
    input (n,v,lst,name)
    n is number of values to sum
    v is equal to n if an average value is required (e.g. for time values, usually it is equal to 1)
    lst is the list of values for combination
    """
    out = []
    delta = 0
    ttemp = 0
    for ind,val in enumerate(lst):
        delta += 1
        ttemp += val # add current value to growing sum
        if delta == n: # critical number is reached
            out.append(ttemp/v) # append sum to list
            delta = 0 # reset critical count and sum
            ttemp = 0
    return out

def binnspectra(dct,n,dec=3,startmz=50.,endmz=2000.):
    """
    sums n mass spectra together into a single spectrum
    
    dct:
        dictionary of timepoints (see mzML.pullspectra output)
        each timepoint is a dictionary with 'x' and 'y' lists
    n:
        number of scans to sum
    dec:
        how many decimals to keep
        default 3
        increasing this does not typically yield better spectra
    startmz:
        lowest mz to sum
        default 50
    endmz:
        highest mz to sum
        default 2000
    """
    import sys
    from _Spectrum import Spectrum
    out = []
    delta = 0
    spec = Spectrum(dec,startmz=startmz,endmz=endmz)
    for time in dct: # for each timepoint
        delta += 1
        sys.stdout.write('\rBinning spectrum #%i/%i  %.1f%%' %(delta,len(dct),float(delta)/float(len(dct))*100.))
        spec.addspectrum(dct[time]['x'],dct[time]['y']) # add spectrum
        if delta == n: # critical number is reached
            out.append(spec.trim(zeros=True)) # append list
            spec.resety() # reset y list in object
            delta = 0 # reset critical sum
    sys.stdout.write(' DONE\n')
    return out
    #for ind,scan in enumerate(lst): # for each pair
    #    delta += 1
    #    sys.stdout.write('\rBinning spectrum #%i/%i  %.1f%%' %(ind+1,len(lst),float(ind+1)/float(len(lst))*100.))
    #    spec.addspectrum(scan['x'],scan['y']) # add spectrum
    #    if delta == n: # critical number is reached
    #        out.append(spec.trim(zeros=True)) # append list
    #        spec.resety() # reset y list in object
    #        delta = 0 # reset critical sum
    #sys.stdout.write(' DONE\n')
    #return out

def bincidspectra(dct,dec=3,startmz=50.,endmz=2000.,threshold=0,fillzeros=False):
    """
    bins mass spectra together based on their collision voltage
    
    lst:
        list of dictionarys corresponding to each scan (see mzML.pullspectra output)
    dec:
        how many decimals to keep
        default 3
        increasing this does not typically yield better spectra
    startmz:
        lowest mz to sum
        default 50
    endmz:
        highest mz to sum
        default 2000
    """
    from _Spectrum import Spectrum
    import sys
    binned = {}
    for time in dct:
        #sys.stdout.write('\rBinning spectrum by CID value #%i/%i  %.1f%%' %(ind+1,len(lst),float(ind+1)/float(len(lst))*100.))
        if binned.has_key(dct[time]['CE']) is False: # generate key if not present
            binned[dct[time]['CE']] = Spectrum(dec,startmz=startmz,endmz=endmz)
        binned[dct[time]['CE']].addspectrum(dct[time]['x'],dct[time]['y'])
    #for ind,scan in enumerate(lst):
    #    sys.stdout.write('\rBinning spectrum by CID value #%i/%i  %.1f%%' %(ind+1,len(lst),float(ind+1)/float(len(lst))*100.))
    #    if binned.has_key(scan['col']) is False: # generate key if not present
    #        binned[scan['col']] = Spectrum(dec,startmz=startmz,endmz=endmz)
    #    binned[scan['col']].addspectrum(scan['x'],scan['y']) # add spectrum existing
    
    #sys.stdout.write(' DONE\n')
    
    if threshold > 0 or fillzeros is True: # if manipulation is called for
        for vol in binned:
            sys.stdout.write('\rZero filling spectrum for %s eV' %`vol`)
            if threshold > 0:
                binned[vol].threshold(threshold) # apply threshold
            if fillzeros is True:
                binned[vol].fillzeros() # fill with zeros
        sys.stdout.write(' DONE\n')
    
    cv = [] # list for collision voltages
    specout = [] # list for spectra
    for vol,spec in sorted(binned.items()):
        sys.stdout.write('\rTrimming spectrum for %s eV' % `vol`)
        cv.append(vol) # append voltage to list
        specout.append(spec.trim()) # append trimmed spectrum to list
    sys.stdout.write(' DONE\n')
    sys.stdout.flush()
    return specout,cv
    
def filepresent(filename,ftype='file'):
    """
    function to check the presense of a file ('file') or directory ('dir')
    in the current working directory
    """
    import os
    if ftype == 'dir':
        if os.path.isdir(filename) == False:
            raise IOError('\nThe directory "%s" could not be located in the current working directory'%(filename))
    if ftype == 'file':
        if os.path.isfile(filename) == False:
            raise IOError('\nThe file "%s" could not be located in the current working directory'%(filename))


def find_all(fname,path):
    """
    Finds all files of a given name within a specified directory.
    Adapted from http://stackoverflow.com/questions/1724693/find-a-file-in-python
    
    Module dependancies: os
    """
    import os
    locations = []
    for root,dirs,files in os.walk(path):
        if fname in files:
            locations.append(os.path.join(root,fname))                   
    return locations

def linmag(vali,magstart,magend,dur):
    """
    funciton for generating a ramp of values that is linear in magnification
    vali: initial value (globally)
    magstart: magnification at the start of the ramp
    magend: magnification at the end of the ramp
    dur: number of steps (duration)
    """
    out = []
    for i in range(dur):
        out.append(float(vali)/((magend-magstart)/dur*i + magstart))
    return out

def linramp(valstart,valend,dur):
    """
    Function for generating a linear ramp of values
    valstart: value at the start of the ramp
    valend: value at the end of the ramp
    dur: number of steps (duration)
    """
    out = []
    for i in range(int(dur)):
        out.append( ((float(valend-valstart))/(float(dur)))*(i) + valstart )
    return out

def lyround(x,basen):
    """
    Function for rounding a given number using a specific base
    based on http://stackoverflow.com/questions/2272149/round-to-5-or-other-number-in-python
    """
    base = basen**(int(len(str(int(x))))-1)
    return int(base * round(float(x)/base))

def mag(initial,final):
    """
    calculate magnification for a value
    """
    return float(initial)/float(final)

def msipoverlay(realspec,simdict,sets,mz,spectrum,ymax,otype='bar'):
    """
    function for plotting and saving a mass spectrum figure with isotope models
    spectrum: 
        list of [[mzvalues],[intvalues]]
    simdict: 
        dictionary of predicted isotope patterns
        each is expected to have the form 'species name':[colour,alpha,[mzlist],[intlist],max intensity]
    sets:
        dictionary of settings (in the form given by the figuresetting fuction)
    mz:
        x axes
    spectrum:
        excel file (for file naming purposes)
    realmax:
        maximum intensity value for figure
    otype:
        type for overlay presentation
        either 'bar' or 'gaussian'        
    """
    import pylab as pl
    import sys
    from _Colour import Colour
    from bisect import bisect_left
    pl.clf() # clear and close figure if open
    pl.close()
    fig = pl.figure(figsize = tuple(sets['size']))
    ax = fig.add_subplot(111)
    
    ax.spines["right"].set_visible(False) #hide right and top spines
    ax.spines["top"].set_visible(False)
    
    if sets['axshow'][0] is False: 
        ax.spines["bottom"].set_visible(False) # hide bottom axis
    if sets['axshow'][1] is False:
        ax.spines["left"].set_visible(False) # hide left axis
    
    for axis in ["top","bottom","left","right"]:
        ax.spines[axis].set_linewidth(sets['axwidth'])    
    
    ax.spines["bottom"].set_position(('axes',-0.01)) #offset x axis 

    font = {'fontname':sets['specfont']} #font parameters for axis/text labels
    tickfont = pl.matplotlib.font_manager.FontProperties(family=sets['specfont'],size=sets['fs']) # font parameters for axis ticks
    
    pl.xlim(mz)
    
    if sets['ymax'] == '100':
        pl.ylim(0,100)
        top = 100
    if sets['ymax'] == 'counts':
        pl.ylim(0,ymax)
        top = ymax
    if type(sets['ymax']) is int:
        pl.ylim(0,sets['ymax'])
        top = sets['ymax']
    
    if otype == 'bar':
        for species in simdict: # generates zeros for bottom of bars (assumes m/z spacing is equal between patterns)
            simdict[species]['zero'] = []
            for i in simdict[species]['x']:
                simdict[species]['zero'].append(0.)
        for species in simdict:
            for subsp in simdict:
                if subsp != species:
                    bl = bisect_left(simdict[subsp]['x'],simdict[species]['x'][-1])
                    if bl > 0 and bl < len(simdict[subsp]['x']): # if species highest m/z is inside subsp list
                        for i in range(bl): # add intensity of species to subsp zeros
                            simdict[subsp]['zero'][i] += simdict[species]['y'][-bl+i]

    if sets['res'][0] is True: #include resolution if specified
        pl.text(mz[1],top,'resolution: '+str(round(sets['res'][1][-1]))[0:-2],fontsize=sets['fs'],horizontalalignment='right',**font)
    if sets['delta'][0] is True: #display mass delta if specified
        pl.text(mz[1],top*0.9,'mass delta: '+str(round(sets['delta'][1],3)),fontsize=sets['fs'],horizontalalignment='right',**font)
    for species in simdict: # plot and label bars
        if otype == 'bar':
            pl.bar(simdict[species]['x'], simdict[species]['y'], sets['res'][1][5]*sets['bw'], alpha = simdict[species]['alpha'], color = Colour(simdict[species]['colour']).mpl, linewidth=0, align='center',bottom=simdict[species]['zero'])
        elif otype == 'gaussian':
            pl.plot(simdict[species]['x'], simdict[species]['y'], alpha = simdict[species]['alpha'], color = Colour(simdict[species]['colour']).mpl, linewidth=sets['lw'])
            pl.fill(simdict[species]['x'], simdict[species]['y'], alpha = simdict[species]['alpha'], color = Colour(simdict[species]['colour']).mpl, linewidth=0)
        if sets['simlabels'] is True: # if label is to be printed
            bpm = max(simdict[species]['y']) # simulation base peak intensity
            bpi = simdict[species]['y'].index(bpm) # index of base peak
            if sets['stats'] is True:
                pl.text(simdict[species]['x'][bpi],top*(1.01),'%s SER: %.2f'%(species,simdict[species]['SER']), fontsize = sets['fs'], alpha = 1, color = Colour(simdict[species]['colour']).mpl,horizontalalignment='center',**font)
            else:
                pl.text(simdict[species]['x'][bpi],top*(1.01),species, fontsize = sets['fs'], alpha = 1, color = Colour(simdict[species]['colour']).mpl,horizontalalignment='center',**font)
    pl.plot(realspec[0],realspec[1], linewidth = sets['lw'], color = 'k') # plot spectrum

    
    # show or hide axis values/labels as specified
    if sets['axvalues'][1] is False:
        pl.tick_params(axis='y', labelleft='off',length=0)
    if sets['axvalues'][1] is True: # y value labels
        pl.tick_params(axis='y', length=sets['axwidth']*3, width=sets['axwidth'], direction='out',right='off')
        for label in ax.get_yticklabels():
            label.set_fontproperties(tickfont)
    if sets['axlabels'][1] is True: # y unit
        if sets['ymax'] == 'counts' or type(sets['ymax']) is int:
            pl.ylabel('intensity (counts)', fontsize = sets['fs'],**font)
        if sets['ymax'] == '100':
            pl.ylabel('relative intensity', fontsize = sets['fs'],**font)
    
    if sets['axvalues'][0] is False: 
        pl.tick_params(axis='x', labelbottom='off',length=0)
    if sets['axvalues'][0] is True: # x value labels
        pl.tick_params(axis='x', length=sets['axwidth']*3, width=sets['axwidth'] ,direction='out',top = 'off')
        for label in ax.get_xticklabels():
            label.set_fontproperties(tickfont) 
    if sets['axlabels'][0] is True: # x unit
        pl.xlabel('m/z', style='italic', fontsize = sets['fs'],**font)
    
    """
    The frame will attempt to autosize to allow for the text size, 
    but you may need to  modify the "bottom" parameter
    """              
    #pl.subplots_adjust(left = (0.10+fs/300.), right = 0.95, bottom = (0.06+fs/300.), top = 0.95)
    pl.tight_layout(pad=0.5)
    pl.subplots_adjust(top = 0.95)
    
    outname = '' # generate tag for filenaming
    for species in simdict:
        outname+=' '+species
    
    pl.plt.savefig(spectrum[0:-5]+' - '+outname+'.'+sets['exten'],dpi=sets['dpiout'],format=sets['exten'],transparent=True)
    sys.stdout.write('Saved figure as "%s" in the working directory' %(spectrum[0:-5]+' - '+outname+'.'+sets['exten']))
    #plt.show()

def normalize(lst,maxval):
    """
    function for normalizing a list of values to a given value
    input:
        lst: list of values
        maxval: value to normalize to
    """
    listmax = max(lst)
    for ind,val in enumerate(lst):
        lst[ind] = float(val)/float(listmax)*maxval
    return lst

def resolution(x,y,index=None):
    """
    Finds the resolution and full width at half max of a spectrum
    x: list of mz values
    y: corresponding list of intensity values
    index: index of maximum intensity (optional; used if the resolution of a specific peak is desired)
    
    returns resolution
    """
    import scipy as sp
    y = sp.asarray(y) # convert to array for efficiency
    if index is None: # find index and value of maximum
        maxy = max(y)
        index = sp.where(y==maxy)[0][0]
    else:
        maxy = y[index]
    halfmax = maxy/2
    indleft = int(index)-1 # generate index counters for left and right walking
    indright = int(index)+1
    while y[indleft] > halfmax: # while intensity is still above halfmax
        #if y[indleft] > y[indleft]+1: # if intensity start increasing (half max was not reached)
        #    raise ValueError('Half max for the left side of the peak could not be determined')
        indleft -= 1
    while y[indright] > halfmax:
        #if y[indright] > y[indright]-1:
        #    raise ValueError('Half max for the right side of the peak could not be determined')
        indright += 1
    return x[index]/(x[indright]-x[indleft]) # return resolution (mz over full width at half max)

#def resolution(x,y,maxindex,realmax):
#    """
#    Function for finding the resolution of a peak given its index in a list and the maximum value
#    x: list of mz values
#    y: corresponding list of intensity values
#    maxindex: index of maximum intensity
#    realmax: value of maximum intensity
#    
#    returns: [halfmax,halfleft,leftmz,halfright,rightmz,delta mz, resolution]
#    """
#    out = []
#    out.append(realmax/2) #0 halfmax
#    for i in range(maxindex):
#        if y[maxindex-i] <= out[0]:
#            out.append(y[maxindex-i]) #1 halfleft
#            out.append(x[maxindex-i]) #2 leftmz
#            break
#    for i in range(len(x)-maxindex):
#        if y[maxindex+i] <= out[0]:
#            out.append(y[maxindex+i]) #3 halfright
#            out.append(x[maxindex+i]) #4 rightmz
#            break
#    out.append(out[4]-out[2]) #5 dmz
#    out.append(x[maxindex]/out[-1]) #6 resolution
#    return out

def sigmafwhm(res,em):
    """
    determines the full width at half max and sigma for a normal distribution
    res is the resolution of the instrument
    em is the mass being calculated
    """
    import math
    fwhm = em/res
    sigma = fwhm/(2*math.sqrt(2*math.log(2))) # based on the equation FWHM = 2*sqrt(2ln2)*sigma
    return fwhm,sigma

def strtolist(string):
    """
    converts a string to a list with more flexibility than string.split()
    """
    out = []
    temp = ''
    brackets = ['(',')','[',']','{','}']
    for char in list(string):
        if char not in brackets and char != ',':
            temp += char
        if char == ',':
            try:
                out.append(int(temp))
            except ValueError:
                out.append(float(temp))
            temp = ''
    if len(temp) != 0: # if there is a weird ending character
        try:
            out.append(int(temp))
        except ValueError:
            out.append(float(temp))
    return out
