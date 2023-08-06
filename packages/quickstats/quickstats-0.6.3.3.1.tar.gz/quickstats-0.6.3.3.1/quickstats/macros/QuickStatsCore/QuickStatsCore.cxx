#ifndef __QuickStatsCore_CXX__
#define __QuickStatsCore_CXX__

#include <map>
#include <string>

#include "RooDataSet.h"
#include "RooAbsPdf.h"

#include "RooFitExt.cxx"

#ifdef __CINT__

#pragma link off all functions;
#pragma link off all globals;
#pragma link off all classes;

#pragma link C++ nestedclasses;
#pragma link C++ nestedtypedefs;

#pragma link C++ namespace RooFitExt;

#pragma link C++ class std::map<std::string, RooDataSet*>+;
//#pragma link C++ class std::map<std::string, RooDataSet*>::*;
#pragma link C++ class std::pair<std::map<string,RooDataSet*>::iterator, bool>+;
//#pragma link C++ class std::pair<std::map<string,RooDataSet*>::iterator, bool>::*+;
#pragma link C++ class std::pair<std::string, RooDataSet*>+;
//#pragma link C++ class std::pair<std::string, RooDataSet*>::*+;
#pragma link C++ class std::map<std::string, RooAbsPdf*>+;
//#pragma link C++ class std::map<std::string, RooAbsPdf*>::*;
#pragma link C++ class std::pair<std::map<string,RooAbsPdf*>::iterator, bool>+;
//#pragma link C++ class std::pair<std::map<string,RooAbsPdf*>::iterator, bool>::*+;
#pragma link C++ class std::pair<std::string, RooAbsPdf*>+;
//#pragma link C++ class std::pair<std::string, RooAbsPdf*>::*+;

#endif

#endif