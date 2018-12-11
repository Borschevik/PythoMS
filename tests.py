"""
a script for validating the functionality of the commonly used scripts
"""
import unittest
import os
import sys
import shutil
from pythoms.mzml import mzML, branch_cvparams, branch_attributes
from pythoms.molecule import Molecule, IPMolecule
from pythoms.spectrum import Spectrum
from PyRSIR import pyrsir
cwd = os.getcwd()


class TestPyRSIR(unittest.TestCase):
    def test(self):
        sys.stdout.write('Testing PyRSIR...')
        shutil.copy(
            cwd + '\\validation_files\\pyrsir_validation.xlsx',
            cwd + '\\validation_files\\pyrsir_validation (backup).xlsx'
        )
        try:
            pyrsir(
                cwd + '\\validation_files\\MultiTest',
                cwd + '\\validation_files\\pyrsir_validation',
                3,
                plot=False,
                verbose=False
            )
        finally:
            shutil.copy(
                cwd + '\\validation_files\\pyrsir_validation (backup).xlsx',
                cwd + '\\validation_files\\pyrsir_validation.xlsx',
            )
            os.remove(cwd + '\\validation_files\\pyrsir_validation (backup).xlsx')
        sys.stdout.write(' PASS\n')


class TestMolecule(unittest.TestCase):
    def setUp(self):
        self.mol = Molecule('L2PdAr+I')
        self.ipmol = IPMolecule(
            'L2PdAr+I',
            ipmethod='multiplicative',
            dropmethod='threshold',
            threshold=0.01,
        )

    def test_molecule(self):
        self.assertEqual(
            self.mol.molecular_formula,
            'C61H51IP3Pd'
        )
        self.assertEqual(
            self.mol.composition,
            {'C': 61, 'H': 51, 'P': 3, 'Pd': 1, 'I': 1}
        )
        self.assertEqual(
            self.mol.molecular_weight,
            1110.300954404405
        )
        self.assertEqual(
            self.mol.monoisotopic_mass,
            1109.12832
        )

    def test_ipmolecule(self):
        self.assertEqual(
            self.ipmol.estimated_exact_mass,
            1109.1303706381723,
        )
        self.assertEqual(
            self.ipmol.barip,
            [[1105.130443, 1106.133823749481, 1107.1290292337153, 1108.1305157201678, 1109.1303706381723,
              1110.1328590930914, 1111.1301978511672, 1112.1325950611867, 1113.1318575059308, 1114.134086933976,
              1115.1370272665604, 1116.140052, 1117.143407],
             [2.287794397621507, 1.5228133756325326, 25.476059354316945, 66.8193866193291, 100.0, 52.65050639843156,
              74.88108058795096, 42.5730473226288, 39.36707265932168, 20.17253048748261, 5.990476280101723,
              1.1848920932846654, 0.16082254122736006]]
        )
        self.ipmol - 'PPh3'  # test subtraction
        self.ipmol + 'PPh3'  # test addition
        mol2 = IPMolecule('N(Et)2(CH2(13C)H2(2H))2')
        self.ipmol + mol2  # test class addition
        self.assertEqual(
            self.ipmol.gaussian_isotope_pattern,
            [[1104.68, 1104.69, 1104.7, 1104.71, 1104.72, 1104.73, 1104.74, 1104.75, 1104.76, 1104.77, 1104.78, 1104.79,
              1104.8, 1104.81, 1104.82, 1104.83, 1104.84, 1104.85, 1104.86, 1104.87, 1104.88, 1104.89, 1104.9, 1104.91,
              1104.92, 1104.93, 1104.94, 1104.95, 1104.96, 1104.97, 1104.98, 1104.99, 1105.0, 1105.01, 1105.02, 1105.03,
              1105.04, 1105.05, 1105.06, 1105.07, 1105.08, 1105.09, 1105.1, 1105.11, 1105.12, 1105.13, 1105.14, 1105.15,
              1105.16, 1105.17, 1105.18, 1105.19, 1105.2, 1105.21, 1105.22, 1105.23, 1105.24, 1105.25, 1105.26, 1105.27,
              1105.28, 1105.29, 1105.3, 1105.31, 1105.32, 1105.33, 1105.34, 1105.35, 1105.36, 1105.37, 1105.38, 1105.39,
              1105.4, 1105.41, 1105.42, 1105.43, 1105.44, 1105.45, 1105.46, 1105.47, 1105.48, 1105.49, 1105.5, 1105.51,
              1105.52, 1105.53, 1105.54, 1105.55, 1105.56, 1105.57, 1105.58, 1105.59, 1105.6, 1105.61, 1105.62, 1105.63,
              1105.64, 1105.65, 1105.66, 1105.67, 1105.68, 1105.69, 1105.7, 1105.71, 1105.72, 1105.73, 1105.74, 1105.75,
              1105.76, 1105.77, 1105.78, 1105.79, 1105.8, 1105.81, 1105.82, 1105.83, 1105.84, 1105.85, 1105.86, 1105.87,
              1105.88, 1105.89, 1105.9, 1105.91, 1105.92, 1105.93, 1105.94, 1105.95, 1105.96, 1105.97, 1105.98, 1105.99,
              1106.0, 1106.01, 1106.02, 1106.03, 1106.04, 1106.05, 1106.06, 1106.07, 1106.08, 1106.09, 1106.1, 1106.11,
              1106.12, 1106.13, 1106.14, 1106.15, 1106.16, 1106.17, 1106.18, 1106.19, 1106.2, 1106.21, 1106.22, 1106.23,
              1106.24, 1106.25, 1106.26, 1106.27, 1106.28, 1106.29, 1106.3, 1106.31, 1106.32, 1106.33, 1106.34, 1106.35,
              1106.36, 1106.37, 1106.38, 1106.39, 1106.4, 1106.41, 1106.42, 1106.43, 1106.44, 1106.45, 1106.46, 1106.47,
              1106.48, 1106.49, 1106.5, 1106.51, 1106.52, 1106.53, 1106.54, 1106.55, 1106.56, 1106.57, 1106.58, 1106.59,
              1106.6, 1106.61, 1106.62, 1106.63, 1106.64, 1106.65, 1106.66, 1106.67, 1106.68, 1106.69, 1106.7, 1106.71,
              1106.72, 1106.73, 1106.74, 1106.75, 1106.76, 1106.77, 1106.78, 1106.79, 1106.8, 1106.81, 1106.82, 1106.83,
              1106.84, 1106.85, 1106.86, 1106.87, 1106.88, 1106.89, 1106.9, 1106.91, 1106.92, 1106.93, 1106.94, 1106.95,
              1106.96, 1106.97, 1106.98, 1106.99, 1107.0, 1107.01, 1107.02, 1107.03, 1107.04, 1107.05, 1107.06, 1107.07,
              1107.08, 1107.09, 1107.1, 1107.11, 1107.12, 1107.13, 1107.14, 1107.15, 1107.16, 1107.17, 1107.18, 1107.19,
              1107.2, 1107.21, 1107.22, 1107.23, 1107.24, 1107.25, 1107.26, 1107.27, 1107.28, 1107.29, 1107.3, 1107.31,
              1107.32, 1107.33, 1107.34, 1107.35, 1107.36, 1107.37, 1107.38, 1107.39, 1107.4, 1107.41, 1107.42, 1107.43,
              1107.44, 1107.45, 1107.46, 1107.47, 1107.48, 1107.49, 1107.5, 1107.51, 1107.52, 1107.53, 1107.54, 1107.55,
              1107.56, 1107.57, 1107.58, 1107.59, 1107.6, 1107.61, 1107.62, 1107.63, 1107.64, 1107.65, 1107.66, 1107.67,
              1107.68, 1107.69, 1107.7, 1107.71, 1107.72, 1107.73, 1107.74, 1107.75, 1107.76, 1107.77, 1107.78, 1107.79,
              1107.8, 1107.81, 1107.82, 1107.83, 1107.84, 1107.85, 1107.86, 1107.87, 1107.88, 1107.89, 1107.9, 1107.91,
              1107.92, 1107.93, 1107.94, 1107.95, 1107.96, 1107.97, 1107.98, 1107.99, 1108.0, 1108.01, 1108.02, 1108.03,
              1108.04, 1108.05, 1108.06, 1108.07, 1108.08, 1108.09, 1108.1, 1108.11, 1108.12, 1108.13, 1108.14, 1108.15,
              1108.16, 1108.17, 1108.18, 1108.19, 1108.2, 1108.21, 1108.22, 1108.23, 1108.24, 1108.25, 1108.26, 1108.27,
              1108.28, 1108.29, 1108.3, 1108.31, 1108.32, 1108.33, 1108.34, 1108.35, 1108.36, 1108.37, 1108.38, 1108.39,
              1108.4, 1108.41, 1108.42, 1108.43, 1108.44, 1108.45, 1108.46, 1108.47, 1108.48, 1108.49, 1108.5, 1108.51,
              1108.52, 1108.53, 1108.54, 1108.55, 1108.56, 1108.57, 1108.58, 1108.59, 1108.6, 1108.61, 1108.62, 1108.63,
              1108.64, 1108.65, 1108.66, 1108.67, 1108.68, 1108.69, 1108.7, 1108.71, 1108.72, 1108.73, 1108.74, 1108.75,
              1108.76, 1108.77, 1108.78, 1108.79, 1108.8, 1108.81, 1108.82, 1108.83, 1108.84, 1108.85, 1108.86, 1108.87,
              1108.88, 1108.89, 1108.9, 1108.91, 1108.92, 1108.93, 1108.94, 1108.95, 1108.96, 1108.97, 1108.98, 1108.99,
              1109.0, 1109.01, 1109.02, 1109.03, 1109.04, 1109.05, 1109.06, 1109.07, 1109.08, 1109.09, 1109.1, 1109.11,
              1109.12, 1109.13, 1109.14, 1109.15, 1109.16, 1109.17, 1109.18, 1109.19, 1109.2, 1109.21, 1109.22, 1109.23,
              1109.24, 1109.25, 1109.26, 1109.27, 1109.28, 1109.29, 1109.3, 1109.31, 1109.32, 1109.33, 1109.34, 1109.35,
              1109.36, 1109.37, 1109.38, 1109.39, 1109.4, 1109.41, 1109.42, 1109.43, 1109.44, 1109.45, 1109.46, 1109.47,
              1109.48, 1109.49, 1109.5, 1109.51, 1109.52, 1109.53, 1109.54, 1109.55, 1109.56, 1109.57, 1109.58, 1109.59,
              1109.6, 1109.61, 1109.62, 1109.63, 1109.64, 1109.65, 1109.66, 1109.67, 1109.68, 1109.69, 1109.7, 1109.71,
              1109.72, 1109.73, 1109.74, 1109.75, 1109.76, 1109.77, 1109.78, 1109.79, 1109.8, 1109.81, 1109.82, 1109.83,
              1109.84, 1109.85, 1109.86, 1109.87, 1109.88, 1109.89, 1109.9, 1109.91, 1109.92, 1109.93, 1109.94, 1109.95,
              1109.96, 1109.97, 1109.98, 1109.99, 1110.0, 1110.01, 1110.02, 1110.03, 1110.04, 1110.05, 1110.06, 1110.07,
              1110.08, 1110.09, 1110.1, 1110.11, 1110.12, 1110.13, 1110.14, 1110.15, 1110.16, 1110.17, 1110.18, 1110.19,
              1110.2, 1110.21, 1110.22, 1110.23, 1110.24, 1110.25, 1110.26, 1110.27, 1110.28, 1110.29, 1110.3, 1110.31,
              1110.32, 1110.33, 1110.34, 1110.35, 1110.36, 1110.37, 1110.38, 1110.39, 1110.4, 1110.41, 1110.42, 1110.43,
              1110.44, 1110.45, 1110.46, 1110.47, 1110.48, 1110.49, 1110.5, 1110.51, 1110.52, 1110.53, 1110.54, 1110.55,
              1110.56, 1110.57, 1110.58, 1110.59, 1110.6, 1110.61, 1110.62, 1110.63, 1110.64, 1110.65, 1110.66, 1110.67,
              1110.68, 1110.69, 1110.7, 1110.71, 1110.72, 1110.73, 1110.74, 1110.75, 1110.76, 1110.77, 1110.78, 1110.79,
              1110.8, 1110.81, 1110.82, 1110.83, 1110.84, 1110.85, 1110.86, 1110.87, 1110.88, 1110.89, 1110.9, 1110.91,
              1110.92, 1110.93, 1110.94, 1110.95, 1110.96, 1110.97, 1110.98, 1110.99, 1111.0, 1111.01, 1111.02, 1111.03,
              1111.04, 1111.05, 1111.06, 1111.07, 1111.08, 1111.09, 1111.1, 1111.11, 1111.12, 1111.13, 1111.14, 1111.15,
              1111.16, 1111.17, 1111.18, 1111.19, 1111.2, 1111.21, 1111.22, 1111.23, 1111.24, 1111.25, 1111.26, 1111.27,
              1111.28, 1111.29, 1111.3, 1111.31, 1111.32, 1111.33, 1111.34, 1111.35, 1111.36, 1111.37, 1111.38, 1111.39,
              1111.4, 1111.41, 1111.42, 1111.43, 1111.44, 1111.45, 1111.46, 1111.47, 1111.48, 1111.49, 1111.5, 1111.51,
              1111.52, 1111.53, 1111.54, 1111.55, 1111.56, 1111.57, 1111.58, 1111.59, 1111.6, 1111.61, 1111.62, 1111.63,
              1111.64, 1111.65, 1111.66, 1111.67, 1111.68, 1111.69, 1111.7, 1111.71, 1111.72, 1111.73, 1111.74, 1111.75,
              1111.76, 1111.77, 1111.78, 1111.79, 1111.8, 1111.81, 1111.82, 1111.83, 1111.84, 1111.85, 1111.86, 1111.87,
              1111.88, 1111.89, 1111.9, 1111.91, 1111.92, 1111.93, 1111.94, 1111.95, 1111.96, 1111.97, 1111.98, 1111.99,
              1112.0, 1112.01, 1112.02, 1112.03, 1112.04, 1112.05, 1112.06, 1112.07, 1112.08, 1112.09, 1112.1, 1112.11,
              1112.12, 1112.13, 1112.14, 1112.15, 1112.16, 1112.17, 1112.18, 1112.19, 1112.2, 1112.21, 1112.22, 1112.23,
              1112.24, 1112.25, 1112.26, 1112.27, 1112.28, 1112.29, 1112.3, 1112.31, 1112.32, 1112.33, 1112.34, 1112.35,
              1112.36, 1112.37, 1112.38, 1112.39, 1112.4, 1112.41, 1112.42, 1112.43, 1112.44, 1112.45, 1112.46, 1112.47,
              1112.48, 1112.49, 1112.5, 1112.51, 1112.52, 1112.53, 1112.54, 1112.55, 1112.56, 1112.57, 1112.58, 1112.59,
              1112.6, 1112.61, 1112.62, 1112.63, 1112.64, 1112.65, 1112.66, 1112.67, 1112.68, 1112.69, 1112.7, 1112.71,
              1112.72, 1112.73, 1112.74, 1112.75, 1112.76, 1112.77, 1112.78, 1112.79, 1112.8, 1112.81, 1112.82, 1112.83,
              1112.84, 1112.85, 1112.86, 1112.87, 1112.88, 1112.89, 1112.9, 1112.91, 1112.92, 1112.93, 1112.94, 1112.95,
              1112.96, 1112.97, 1112.98, 1112.99, 1113.0, 1113.01, 1113.02, 1113.03, 1113.04, 1113.05, 1113.06, 1113.07,
              1113.08, 1113.09, 1113.1, 1113.11, 1113.12, 1113.13, 1113.14, 1113.15, 1113.16, 1113.17, 1113.18, 1113.19,
              1113.2, 1113.21, 1113.22, 1113.23, 1113.24, 1113.25, 1113.26, 1113.27, 1113.28, 1113.29, 1113.3, 1113.31,
              1113.32, 1113.33, 1113.34, 1113.35, 1113.36, 1113.37, 1113.38, 1113.39, 1113.4, 1113.41, 1113.42, 1113.43,
              1113.44, 1113.45, 1113.46, 1113.47, 1113.48, 1113.49, 1113.5, 1113.51, 1113.52, 1113.53, 1113.54, 1113.55,
              1113.56, 1113.57, 1113.58, 1113.59, 1113.6, 1113.61, 1113.62, 1113.63, 1113.64, 1113.65, 1113.66, 1113.67,
              1113.68, 1113.69, 1113.7, 1113.71, 1113.72, 1113.73, 1113.74, 1113.75, 1113.76, 1113.77, 1113.78, 1113.79,
              1113.8, 1113.81, 1113.82, 1113.83, 1113.84, 1113.85, 1113.86, 1113.87, 1113.88, 1113.89, 1113.9, 1113.91,
              1113.92, 1113.93, 1113.94, 1113.95, 1113.96, 1113.97, 1113.98, 1113.99, 1114.0, 1114.01, 1114.02, 1114.03,
              1114.04, 1114.05, 1114.06, 1114.07, 1114.08, 1114.09, 1114.1, 1114.11, 1114.12, 1114.13, 1114.14, 1114.15,
              1114.16, 1114.17, 1114.18, 1114.19, 1114.2, 1114.21, 1114.22, 1114.23, 1114.24, 1114.25, 1114.26, 1114.27,
              1114.28, 1114.29, 1114.3, 1114.31, 1114.32, 1114.33, 1114.34, 1114.35, 1114.36, 1114.37, 1114.38, 1114.39,
              1114.4, 1114.41, 1114.42, 1114.43, 1114.44, 1114.45, 1114.46, 1114.47, 1114.48, 1114.49, 1114.5, 1114.51,
              1114.52, 1114.53, 1114.54, 1114.55, 1114.56, 1114.57, 1114.58, 1114.59, 1114.6, 1114.61, 1114.62, 1114.63,
              1114.64, 1114.65, 1114.66, 1114.67, 1114.68, 1114.69, 1114.7, 1114.71, 1114.72, 1114.73, 1114.74, 1114.75,
              1114.76, 1114.77, 1114.78, 1114.79, 1114.8, 1114.81, 1114.82, 1114.83, 1114.84, 1114.85, 1114.86, 1114.87,
              1114.88, 1114.89, 1114.9, 1114.91, 1114.92, 1114.93, 1114.94, 1114.95, 1114.96, 1114.97, 1114.98, 1114.99,
              1115.0, 1115.01, 1115.02, 1115.03, 1115.04, 1115.05, 1115.06, 1115.07, 1115.08, 1115.09, 1115.1, 1115.11,
              1115.12, 1115.13, 1115.14, 1115.15, 1115.16, 1115.17, 1115.18, 1115.19, 1115.2, 1115.21, 1115.22, 1115.23,
              1115.24, 1115.25, 1115.26, 1115.27, 1115.28, 1115.29, 1115.3, 1115.31, 1115.32, 1115.33, 1115.34, 1115.35,
              1115.36, 1115.37, 1115.38, 1115.39, 1115.4, 1115.41, 1115.42, 1115.43, 1115.44, 1115.45, 1115.46, 1115.47,
              1115.48, 1115.49, 1115.5, 1115.51, 1115.52, 1115.53, 1115.54, 1115.55, 1115.56, 1115.57, 1115.58, 1115.59,
              1115.6, 1115.61, 1115.62, 1115.63, 1115.64, 1115.65, 1115.66, 1115.67, 1115.68, 1115.69, 1115.7, 1115.71,
              1115.72, 1115.73, 1115.74, 1115.75, 1115.76, 1115.77, 1115.78, 1115.79, 1115.8, 1115.81, 1115.82, 1115.83,
              1115.84, 1115.85, 1115.86, 1115.87, 1115.88, 1115.89, 1115.9, 1115.91, 1115.92, 1115.93, 1115.94, 1115.95,
              1115.96, 1115.97, 1115.98, 1115.99, 1116.0, 1116.01, 1116.02, 1116.03, 1116.04, 1116.05, 1116.06, 1116.07,
              1116.08, 1116.09, 1116.1, 1116.11, 1116.12, 1116.13, 1116.14, 1116.15, 1116.16, 1116.17, 1116.18, 1116.19,
              1116.2, 1116.21, 1116.22, 1116.23, 1116.24, 1116.25, 1116.26, 1116.27, 1116.28, 1116.29, 1116.3, 1116.31,
              1116.32, 1116.33, 1116.34, 1116.35, 1116.36, 1116.37, 1116.38, 1116.39, 1116.4, 1116.41, 1116.42, 1116.43,
              1116.44, 1116.45, 1116.46, 1116.47, 1116.48, 1116.49, 1116.5, 1116.51, 1116.52, 1116.53, 1116.54, 1116.55,
              1116.56, 1116.57, 1116.58, 1116.59, 1116.6, 1116.61, 1116.62, 1116.63, 1116.64, 1116.65, 1116.66, 1116.67,
              1116.68, 1116.69, 1116.7, 1116.71, 1116.72, 1116.73, 1116.74, 1116.75, 1116.76, 1116.77, 1116.78, 1116.79,
              1116.8, 1116.81, 1116.82, 1116.83, 1116.84, 1116.85, 1116.86, 1116.87, 1116.88, 1116.89, 1116.9, 1116.91,
              1116.92, 1116.93, 1116.94, 1116.95, 1116.96, 1116.97, 1116.98, 1116.99, 1117.0, 1117.01, 1117.02, 1117.03,
              1117.04, 1117.05, 1117.06, 1117.07, 1117.08, 1117.09, 1117.1, 1117.11, 1117.12, 1117.13, 1117.14, 1117.15,
              1117.16, 1117.17, 1117.18, 1117.19, 1117.2, 1117.21, 1117.22, 1117.23, 1117.24, 1117.25, 1117.26, 1117.27,
              1117.28, 1117.29, 1117.3, 1117.31, 1117.32, 1117.33, 1117.34, 1117.35, 1117.36, 1117.37, 1117.38, 1117.39,
              1117.4, 1117.41, 1117.42, 1117.43, 1117.44, 1117.45, 1117.46, 1117.47, 1117.48, 1117.49, 1117.5, 1117.51,
              1117.52, 1117.53, 1117.54, 1117.55, 1117.56, 1117.57, 1117.58, 1117.59, 1117.6],
             [0.0, 2.287794397621507, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              1.5228133756325326, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              25.476059354316945, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              66.8193866193291, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 100.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 52.65050639843156, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 74.88108058795096, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 42.5730473226288, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 39.36707265932168, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 20.17253048748261, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 5.990476280101723, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 1.1848920932846654, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.16082254122736006, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

        )


class TestmzML(unittest.TestCase):
    def test_mzml(self):
        sys.stdout.write('Testing mzML class...')
        mzml = mzML(
            cwd + '\\validation_files\\MultiTest',
            verbose=False
        )
        self.assertEqual(  # check that the correct function keys were pulled
            mzml.functions.keys(),
            {1, 3, 4},
        )

        @mzml.foreachchrom
        def testperchrom(chromatogram):
            attr = branch_attributes(chromatogram)
            return attr['id']

        self.assertEqual(  # test chromatogram decorator
            testperchrom(),
            [u'TIC', u'SRM SIC Q1=200 Q3=100 function=2 offset=0']
        )

        @mzml.foreachscan
        def testperspec(spectrum):
            p = branch_cvparams(spectrum)
            return p["MS:1000016"].value

        self.assertEqual(  # test spectrum decorator
            testperspec(),
            [0.0171000008, 0.135733336, 0.254333347, 0.372983336, 0.491699994, 0.0510833338, 0.169750005,
             0.288383335, 0.407000005, 0.525833309, 0.0847499967, 0.20341666, 0.322033346, 0.440683335]
        )

        self.assertEqual(  # test intensity summing
            sum(mzml.sum_scans()[1]),
            162806964
        )

        self.assertEqual(  # test scan indexing
            sum((mzml[2])[1]),
            6742121
        )

        self.assertEqual(  # test time indexing
            sum((mzml[0.01])[1]),
            56270834
        )


def test_xlsx():
    sys.stdout.write('Testing XLSX class...')
    from pythoms.xlsx import XLSX
    xlfile = XLSX(
        cwd + '\\validation_files\\xlsx_validation',
        verbose=False
    )
    spec, xunit, yunit = xlfile.pullspectrum('example MS spectrum')
    multispec = xlfile.pullmultispectrum('example multi-spectrum')
    rsimparams = xlfile.pullrsimparams()
    xlout = XLSX(
        cwd + '\\validation_files\\xlsxtestout.xlsx',
        create=True,
        verbose=False
    )
    xlout.writespectrum(spec[0], spec[1], 'test single spectrum out', xunit, yunit)
    for key, val in sorted(multispec.items()):
        xlout.writemultispectrum(multispec[key]['x'], multispec[key]['y'], multispec[key]['xunit'],
                                 multispec[key]['yunit'], 'Function Chromatograms', key)
    xlout.save()
    os.remove(
        cwd + '\\validation_files\\xlsxtestout.xlsx'
    )
    sys.stdout.write(' PASS\n')


class TestSpectrum(unittest.TestCase):
    def test_spectrum(self):
        spec = Spectrum(3)
        spec.add_value(479.1, 1000)
        self.assertEqual(
            spec.trim(),
            [[479.1], [1000]]
        )

        spec2 = Spectrum(3)
        spec2.add_value(443.1, 1000)
        self.assertEqual(
            spec2.trim(),
            [[443.1], [1000]]
        )
        spec += spec2
        self.assertEqual(
            spec.trim(),
            [[443.1, 479.1], [1000, 1000]]
        )
        spec3 = Spectrum(3, start=50, end=2500)
        spec3.add_value(2150.9544, 1000)
        self.assertEqual(
            spec3.trim(),
            [[2150.954], [1000]]
        )
        spec += spec3

        self.assertEqual(
            spec.trim(True),
            [[50.0, 443.1, 479.1, 2150.954, 2500], [0.0, 1000, 1000, 1000, 0.0]]
        )
        spec.end = 2100.
        self.assertEqual(
            spec.trim(),
            [[443.1, 479.1], [1000, 1000]]
        )


if __name__ == '__main__':
    if os.path.dirname(os.path.realpath(__file__)) not in sys.path:
        sys.path.append(os.path.dirname(os.path.realpath(__file__)))
        sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '\\validation_files')
    unittest.main(verbosity=2)
