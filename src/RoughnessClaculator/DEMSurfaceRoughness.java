package RoughnessClaculator;

import org.geotools.coverage.grid.GridCoverage2D;
import org.geotools.coverage.grid.GridCoverageFactory;
import org.geotools.gce.geotiff.GeoTiffReader;
import org.geotools.geometry.Envelope2D;

import java.awt.image.Raster;
import java.io.File;

public class DEMSurfaceRoughness {

    public static void main(String[] args) {
        try {
            File demFile = new File("pfad_zu_deinem_dem.tif");
            GeoTiffReader reader = new GeoTiffReader(demFile);

            GridCoverage2D coverage = reader.read(null);
            Raster data = coverage.getRenderedImage().getData();

            int width = data.getWidth();
            int height = data.getHeight();

            // Erstellen eines Rasters zur Speicherung der Rauheitswerte
            double[] roughness = new double[width * height];

            // Berechnung der Rauheit für jedes Pixel
            for (int y = 1; y < height - 1; y++) {
                for (int x = 1; x < width - 1; x++) {
                    roughness[y * width + x] = calculateRoughness(data, x, y);
                }
            }

            // Hier könntest du die Rauheitswerte weiter verarbeiten oder speichern
            System.out.println("Rauheit berechnet.");

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static double calculateRoughness(Raster data, int x, int y) {
        double sum = 0.0;
        double mean;
        double sumSquare = 0.0;
        int count = 0;

        // Durchlaufen eines 3x3-Fensters um das zentrale Pixel
        for (int dx = -1; dx <= 1; dx++) {
            for (int dy = -1; dy <= 1; dy++) {
                double value = data.getSampleDouble(x + dx, y + dy, 0);
                sum += value;
                count++;
            }
        }

        mean = sum / count;

        // Berechnung der Standardabweichung
        for (int dx = -1; dx <= 1; dx++) {
            for (int dy = -1; dy <= 1; dy++) {
                double value = data.getSampleDouble(x + dx, y + dy, 0);
                sumSquare += Math.pow(value - mean, 2);
            }
        }

        return Math.sqrt(sumSquare / count);
    }
}

