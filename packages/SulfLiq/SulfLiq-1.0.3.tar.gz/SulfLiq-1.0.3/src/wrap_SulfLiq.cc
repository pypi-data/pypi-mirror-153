#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include "SulfLiq.h"

#include <iostream>
#include <vector>

namespace py = pybind11;

class pySulfLiq : public SulfLiq {
public:
	using SulfLiq::SulfLiq;

	void setComps(std::vector<double>& c) {
		double *lcomps = c.data();
		SulfLiq::setComps(lcomps);
	}
	void setSpecs(std::vector<double>& c) {
		double *lcomps = c.data();
		SulfLiq::setSpecs(lcomps);
	}
	void setSpecsFull(std::vector<double>& c) {
		double *lcomps = c.data();
		SulfLiq::setSpecsFull(lcomps);
	}
	void setCompWeights(std::vector<double>& c) {
		double *lcomps = c.data();
		SulfLiq::setCompWeights(lcomps);
	}
	void setCompWtPct(std::vector<double>& c) {
		double *lcomps = c.data();
		SulfLiq::setCompWtPct(lcomps);
	}
	void setElements(std::vector<double>& c) {
		double *lcomps = c.data();
		SulfLiq::setElements(lcomps);
	}
	std::vector<double> getSpecs() {
		int n = getNspec();
		std::vector<double> v(n);
		SulfLiq::getSpecs(v.data());
		return v;
	}
	std::vector<double> getComps() {
		int n = getNcomp();
		std::vector<double> v(n);
		SulfLiq::getComps(v.data());
		return v;
	}
	std::vector<double> getCompWeights() {
		int n = getNcomp();
		std::vector<double> v(n);
		SulfLiq::getCompWeights(v.data());
		return v;
	}
	std::vector<double> getCompWtPct() {
		int n = getNcomp();
		std::vector<double> v(n);
		SulfLiq::getCompWtPct(v.data());
		return v;
	}
	std::vector<double> getElements() {
		int n = 107;
		std::vector<double> v(n);
		SulfLiq::getElements(v.data());
		return v;
	}
	std::vector<std::vector<double>> getd2Gdm2() {
		int n = getNcomp();
		std::vector<std::vector<double>> m(n, std::vector<double> (n));
		double *result[n];
		for (int i=0; i<n; i++) {
			result[i] = m[i].data();
		}
		SulfLiq::getd2Gdm2(result);
		return m;
	}
	std::vector<double> getdSdm() {
		int n = getNcomp();
		std::vector<double> v(n);
		SulfLiq::getdSdm(v.data());
		return v;
	}
	std::vector<std::vector<double>> getd2Sdm2() {
		int n = getNcomp();
		std::vector<std::vector<double>> m(n, std::vector<double> (n));
		double *result[n];
		for (int i=0; i<n; i++) {
			result[i] = m[i].data();
		}
		SulfLiq::getd2Sdm2(result);
		return m;
	}
	std::vector<double> getActivity() {
		int n = getNcomp();
		std::vector<double> v(n);
		SulfLiq::getActivity(v.data());
		return v;
	}
	std::vector<double> getdGdm() {
		int n = getNcomp();
		std::vector<double> v(n);
		SulfLiq::getdGdm(v.data());
		return v;
	}
	std::vector<double> getdCpdm() {
		int n = getNcomp();
		std::vector<double> v(n);
		SulfLiq::getdCpdm(v.data());
		return v;
	}
	std::vector<double> getdVdm() {
		int n = getNcomp();
		std::vector<double> v(n);
		SulfLiq::getdVdm(v.data());
		return v;
	}
	std::vector<std::vector<double>> getd2Vdm2() {
		int n = getNcomp();
		std::vector<std::vector<double>> m(n, std::vector<double> (n));
		double *result[n];
		for (int i=0; i<n; i++) {
			result[i] = m[i].data();
		}
		SulfLiq::getd2Vdm2(result);
		return m;
	}
	std::vector<double> getd2VdmdT() {
		int n = getNcomp();
		std::vector<double> v(n);
		SulfLiq::getd2VdmdT(v.data());
		return v;
	}
	std::vector<double> getd2VdmdP() {
		int n = getNcomp();
		std::vector<double> v(n);
		SulfLiq::getd2VdmdP(v.data());
		return v;
	}
};

PYBIND11_MODULE(SulfLiq, m) {
    py::class_<pySulfLiq>(m, "pySulfLiq")
    	.def(py::init<>())
    	// setting, getting routines
    	.def("setTK", &pySulfLiq::setTk, "Set temperature in K")
        .def("setPa", &pySulfLiq::setPa, "Set pressure in Pa")
        .def("getTK", &pySulfLiq::getTk, "Returns temperature in K")
        .def("getPa", &pySulfLiq::getPa, "Returns pressure in Pa")
        .def("resetTPbounds", &pySulfLiq::resetTPbounds, "Reset default bounds for temperature and pressure")
        .def("getNspec", &pySulfLiq::getNspec, "Returns number of species")
        .def("getSpecName", &pySulfLiq::getSpecName, "Returns species name")
        .def("getSpecFormula", &pySulfLiq::getSpecFormula, "Returns species formula")
        //
        .def("getNcomp", &pySulfLiq::getNcomp, "Returns number of components in system")
        .def("getCompNo", &pySulfLiq::getCompNo, "Returns component number for input string.  Match must be exact")
        .def("getCompName", &pySulfLiq::getCompName, "Returns ith component name")
        .def("getCompFormula", &pySulfLiq::getCompFormula, "Returns ith component formula")
        //
        .def("setMoles", &pySulfLiq::setMoles, "Set total moles of components")
        .def("setMass", &pySulfLiq::setMass, "Set total mass of solution in grams")
        .def("getMoles", &pySulfLiq::getMoles, "Returns sum of moles of components")
        .def("getMass", &pySulfLiq::getMass, "Returns total mass of phase in grams")
        .def("setComps", &pySulfLiq::setComps, "Set moles of components with vector")
        .def("setSpecs", &pySulfLiq::setSpecs, "Set moles of species (perhaps metastable, zeros ignored)")
        .def("setSpecsFull", &pySulfLiq::setSpecsFull, "Set moles of species (perhaps metastable, zeros used)")
        .def("getSpecs", &pySulfLiq::getSpecs, "Returns species abundances in moles")
        .def("setCompWeights", &pySulfLiq::setCompWeights, "Sets component weights in kg")
        .def("setCompWtPct", &pySulfLiq::setCompWtPct, "Sets components from vector in weight percent (nmoles set to 1.0)")
        .def("setElements", &pySulfLiq::setElements, "Set moles of elements")
        .def("getComps", &pySulfLiq::getComps, "Returns component moles in caller-allocated vector")
        .def("getCompWeights", &pySulfLiq::getCompWeights, "Returns component grams in caller-allocated vector")
        .def("getCompWtPct", &pySulfLiq::getCompWtPct, "Returns components in weight percent.  Does not allocate space")
        .def("getElements", &pySulfLiq::getElements, "Returns moles of elements in caller-allocated space")
        //
        .def("supressSpecies", &pySulfLiq::supressSpecies, "Suppress formation of species i. Cannot supress component")
        .def("setSpeciateTolerance", &pySulfLiq::setSpeciateTolerance, "Set fractional convergence tolerance for homogeneous equilibrium calculation")
        .def("update", &pySulfLiq::update, "Calculates homogenious equilibrium. Replaces dummy routine in Phase")
        .def("getSpecCalcErr", &pySulfLiq::getSpecCalcErr, "Returns error in last homogenious speciation calculation (Joules)")
        .def("isUpdated", &pySulfLiq::isUpdated, "Returns boolean indicating if hom. eq. calculated for curr. conditions")
        .def("isStable", &pySulfLiq::isStable, "Checks for phase stability by Hessian test")
        .def_readwrite("verbose", &SulfLiq::verbose, "Flag for verbose progress output during equilibration. 0 by default")
        .def("printAll", &SulfLiq::printAll, "prints most properties of phase")
        //
        .def("setFugacity", (int (pySulfLiq::*)(double, double)) &pySulfLiq::setFugacity, "Adjusts O and S corresponding to input log10(fo2) and log10(fS2)")
        .def("setFugacity", (int (pySulfLiq::*)(double, double, int)) &pySulfLiq::setFugacity, "Adjusts O and S corresponding to input log10(fo2) and log10(fS2), if verbose = true then print progres")
        .def("setlogfo2", &pySulfLiq::setlogfo2, "Set oxygen fugacity")
        .def("setlogfs2", &pySulfLiq::setlogfs2, "Set sulfur fugacity")
        .def("getlogfo2", &pySulfLiq::getlogfo2, "Returns oxygen fugacity")
        .def("getlogfs2", &pySulfLiq::getlogfs2, "Set sulfur fugacity")
        //
        .def("getGibbs", &pySulfLiq::getGibbs, "Returns Gibbs free energy in Joules")
        .def("getGmix", &pySulfLiq::getGmix, "Returns mixing component of Gibbs free energy in Joules")
        //
        .def("getMu0", (double (pySulfLiq::*)(int)) &pySulfLiq::getMu0, "Returns standard-state chemical potentials at T and P")
        .def("getMu", (double (pySulfLiq::*)(int)) &pySulfLiq::getMu, "Returns chemical potential of component in J/mole")
        .def("getActivity", (double (pySulfLiq::*)(int)) &pySulfLiq::getActivity, "Returns activity of component in J/mole")
        .def("getActivity", (std::vector<double> (pySulfLiq::*)(void)) &pySulfLiq::getActivity, "Returns activity of component in J/mole")
        .def("getCompMu", &pySulfLiq::getCompMu, "Returns chemical potential of component in J/mole")
        .def("getSpecMu", &pySulfLiq::getSpecMu, "Returns chemical potential of species in J/mole")
        .def("getdMudX", &pySulfLiq::getdMudX, "Returns dMu[i]/dX[j] for components")
        //
        .def("getdGdm", &pySulfLiq::getdGdm, "Returns derivative of Gibbs free energy with respect to moles (Joules/mole)")
        .def("getd2Gdm2", &pySulfLiq::getd2Gdm2, "Returns second derivative of G with respect to components")
        //
        .def("getEnthalpy", &pySulfLiq::getEnthalpy, "Returns enthalpy in Joules")
        .def("getHmix", &pySulfLiq::getHmix, "Returns enthalpy of mixing in Joules")
        //
        .def("getEntropy", &pySulfLiq::getEntropy, "Returns entropy in Joules/Kelvin")
        .def("getdSdm", &pySulfLiq::getdSdm, "Returns derivative of entropy with respect to components")
        .def("getd2Sdm2", &pySulfLiq::getd2Sdm2, "Returns second derivative of entropy with respect to components")
        .def("getSmix", &pySulfLiq::getSmix, "Returns entropy of mixing in Joules/Kelvin")
        //
        .def("getCp", &pySulfLiq::getCp, "Returns heat capacity")
        .def("getdCpdT", &pySulfLiq::getdCpdT, "Returns dCp/dT")
        .def("getdCpdm", &pySulfLiq::getdCpdm, "Returns derivative of Cp with respect to composition")
        .def("getCpmix", &pySulfLiq::getCpmix, "Returns heat capacity of mixing")
        .def("getdCpdTmix", &pySulfLiq::getdCpdTmix, "Returns dCp/dT of mixing")
        //
        .def("getVolume", &pySulfLiq::getVolume, "Returns volume in m^3")
        .def("getdVdm", &pySulfLiq::getdVdm, "Returns derivative of volume with respect to composition")
        .def("getd2Vdm2", &pySulfLiq::getd2Vdm2, "Returns second derivative of volume with respect to composition")
        .def("getdVdT", &pySulfLiq::getdVdT, "Returns dV/dT in m^3/K")
        .def("getVmix", &pySulfLiq::getVmix, "Returns volume of mixing in cubic meters (Joules/Pascal)")
        .def("getdVdTmix", &pySulfLiq::getdVdTmix, "Returns dV/dT of mixing in M^3/K")
        .def("getdVdP", &pySulfLiq::getdVdP, "Returns dV/dP in M^3/Pascal")
        .def("getd2VdT2", &pySulfLiq::getd2VdT2, "Returns d2V/dT2 in M^3/Kelvin^2")
        .def("getd2VdTdP", &pySulfLiq::getd2VdTdP, "Returns d2V/dTdP in M^3/KelvinPascal")
        .def("getd2VdP2", &pySulfLiq::getd2VdP2, "Returns d2V/dP2 in M^3/Pascal^2")
        .def("getd2VdmdT", &pySulfLiq::getd2VdmdT, "Returns d2VdmdT in M^3/KelvinMole")
        .def("getd2VdmdP", &pySulfLiq::getd2VdmdP, "Returns d2VdmdP in M^3/PascalMole")
        .def("__repr__", [](const pySulfLiq &s) {
        	return "Victor Kress sulfide liquid model. Model and data from Kress (1997, 2000, 2001).";
        })
        ; 
    }
