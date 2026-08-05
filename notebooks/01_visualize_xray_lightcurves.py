import os
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.time import Time

def plot_lightcurve():
    # Use the extracted fits file path
    fits_file = r"d:\NFS's Projects\Solar flare forecasting & nowcasting using Aditya-L1 X-ray data\datasets\HEL1OS_sample\2023\12\01\HLS_20231130_235953_28794sec_lev1_V111\cdte\lightcurve_cdte1.fits"
    
    # We will use the 5th HDU which corresponds to the broad band: 1.80 KEV TO 90.00 KEV
    # As identified from our previous inspection.
    with fits.open(fits_file) as hdul:
        data = hdul[5].data
        band_name = hdul[5].name
        
    mjd = data['MJD']
    ctr = data['CTR']
    
    # Convert MJD to datetime objects for better plotting
    t = Time(mjd, format='mjd')
    datetimes = t.datetime
    
    plt.figure(figsize=(12, 6))
    plt.plot(datetimes, ctr, label=band_name, color='orange', linewidth=1)
    
    plt.xlabel('Time (UTC)')
    plt.ylabel('Count Rate (Counts/s)')
    plt.title('Aditya-L1 HEL1OS X-ray Lightcurve (CdTe1)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save to artifacts folder for the walkthrough
    artifact_dir = r"C:\Users\NFS Photographer\.gemini\antigravity-ide\brain\79d3e34d-4b55-4524-a972-89a9161d8826"
    plot_path = os.path.join(artifact_dir, "hel1os_lightcurve_sample.png")
    plt.savefig(plot_path, dpi=150)
    print(f"Plot saved to {plot_path}")

if __name__ == "__main__":
    plot_lightcurve()
