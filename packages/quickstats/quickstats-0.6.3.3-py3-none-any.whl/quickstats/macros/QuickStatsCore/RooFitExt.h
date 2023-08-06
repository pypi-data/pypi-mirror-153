#ifndef __RooFitExtension_H__
#define __RooFitExtension_H__

#include <regex>
#include <string>
#include <vector>
#include <sstream>
#include <stdexcept>

#include "TString.h"
#include "RooArgSet.h"
#include "RooArgList.h"
#include "RooAbsArg.h"
#include "RooAbsPdf.h"
#include "RooProdPdf.h"
#include "RooProduct.h"
#include "RooDataSet.h"
#include "RooFormula.h"
#include "RooFormulaVar.h"
#include "RooPrintable.h"
#include "RooListProxy.h"
#include "RooHistFunc.h"
#include "RooStats/HistFactory/FlexibleInterpVar.h"

namespace RooFitExt{
    
    struct ConstraintSet {
      RooArgList pdfs;
      RooArgList nuis;
      RooArgList globs;
      ConstraintSet(){
          pdfs = RooArgList();
          nuis = RooArgList();
          globs = RooArgList();
      }
    };
    
    struct RooArgSetStrData{
      std::vector<std::string> names;
      std::vector<std::string> classes;
      std::vector<std::string> definitions;
      RooArgSetStrData(){
          names       = std::vector<std::string>();
          classes     = std::vector<std::string>();
          definitions = std::vector<std::string>();
      }
      RooArgSetStrData(unsigned int size){
          names       = std::vector<std::string>(size);
          classes     = std::vector<std::string>(size);
          definitions = std::vector<std::string>(size);
      }
    };
    
    const std::vector<std::string> kConstrPdfClsList{"RooGaussian", "RooLognormal", "RooGamma", "RooPoisson", "RooBifurGauss"};
    
    void unfoldProdPdfComponents(const RooProdPdf& prod_pdf, RooArgSet& components, int recursion_count=0,
                                 const int& recursion_limit=50);
    RooRealVar* isolateConstraintEx(const RooAbsPdf& pdf, const RooArgSet& constraints);
    RooRealVar* isolateConstraint(const RooAbsPdf& pdf, const RooArgSet& constraints);
    ConstraintSet pairConstraints(const RooArgSet& constraintPdfs, const RooArgSet& nuisanceParams,
                                  const RooArgSet& globalObs);
    void unfoldConstraints(const RooArgSet& constraintPdfs, RooArgSet& observables,
                           RooArgSet& nuisanceParams, RooArgSet* unfoldedConstraintPdfs,
                           const std::vector<std::string>constrPdfClsList=kConstrPdfClsList,
                           int recursion_count=0, const int& recursion_limit=50,
                           const bool &stripDisconnected=false);
    std::string getReconstructedFormulaStr(const RooFormula &formula);
    std::string getFunctionStrRepr(RooFormulaVar &formula_var);
    std::string getFunctionStrRepr(RooProduct &product_func);
    std::string getCorrectPrintArgs(RooHistFunc& arg);
    std::string getCorrectPrintArgs(RooStats::HistFactory::FlexibleInterpVar& arg);
    std::string getCorrectPrintArgs(RooFormulaVar& arg);
    std::string getCorrectPrintArgs(RooPrintable& arg);
    std::string getPrintStr(RooAbsArg *printableObj, Int_t contents=-1, Int_t style=-1,
                            const TString &indent="", const bool& strip_newline=true,
                            const bool& correction=true);
    RooArgSetStrData getStrData(RooArgSet &components, const bool& fill_classes=false,
                                const bool& fill_definitions=false, Int_t contents=-1,
                                Int_t style=-1, const TString &indent="",
                                const bool& correction=true);
};

        
#endif        
