from application_driver import ApplicationDriver

# TODO: Write documentation


def main():
    input_path = '/Users/lukasbatschelet/Library/CloudStorage/OneDrive-UniversitaetBern/Studium/FS24/Geoprocessing-II/Projektarbeit_Fotogrammetrie/20240415_Grundlagen/202311xx_Rohdaten/20231116_DEM_Sammler_Obermad_0.05m.tif'
    output_path = '/Users/lukasbatschelet/Library/CloudStorage/OneDrive-UniversitaetBern/Studium/FS24/Geoprocessing-II/Projektarbeit_Fotogrammetrie/05_Output/20231116_DEM_Sammler_Obermad_0.05m.tif'
    driver = ApplicationDriver(input_path, output_path)
    driver.run()


if __name__ == '__main__':
    main()
