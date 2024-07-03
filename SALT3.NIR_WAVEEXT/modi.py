import numpy as np
from FileRead import readcol
import glob
from DavidsNM import save_img

for fl in glob.glob("origs/*dat"):
    [phase, wave, flux] = readcol(fl, 'fff')
    if len(phase) > 0:
        unique_phase = np.unique(phase)
        unique_wave = np.unique(wave)
        assert all(unique_wave == np.sort(unique_wave))
        
        flux2d = np.reshape(flux, [len(unique_phase), len(unique_wave)])
        

        d_wave = np.median(unique_wave[1:] - unique_wave[:-1])
        print("d_wave", d_wave)

        new_waves = np.arange(unique_wave[0] - d_wave*np.around((unique_wave[0] - 800)/d_wave), unique_wave[0], d_wave)

        unique_wave = np.concatenate((new_waves, unique_wave))
        print("unique_wave", list(unique_wave))

        new_flux = (np.ones([len(new_waves), len(unique_phase)])*flux2d[:,0]).T
        print("new_flux", new_flux.shape)
        print("flux2d", flux2d.shape)

        flux2d = np.concatenate((   new_flux, flux2d   ), axis = 1)
        
        



        newfl = fl.split("/")[-1]
        assert newfl != fl

        save_img(flux2d, "flux2d_" + newfl.split(".")[0] + ".fits")

        
        f = open(newfl, 'w')
        for i in range(len(unique_phase)):
            for j in range(len(unique_wave)):
                f.write(str(unique_phase[i]) + "  " + str(unique_wave[j]) + "  " + str(flux2d[i, j]) + '\n')
        f.close()
        
        """
        wave = concatenate((wave[:i+1], new_waves, wave[i+1:]))
        phase = concatenate((phase[:i+1], new_phases, phase[i+1:]))
        flux = concatenate((flux[:i+1], new_fluxes, flux[i+1:]))
            

        f = open(fl, 'w')
        for i in range(len(wave)):
            f.write(str(phase[i]) + "  " + str(wave[i]) + "  " + str(flux[i]) + '\n')
            
        f.close()
        """
    else:
        print(fl, "By hand!")

        
