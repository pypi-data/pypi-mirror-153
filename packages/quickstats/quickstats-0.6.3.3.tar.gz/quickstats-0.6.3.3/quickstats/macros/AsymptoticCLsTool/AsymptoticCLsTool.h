#ifndef ASYMPTOTIC_CLS_TOOL
#define ASYMPTOTIC_CLS_TOOL

#include <iostream>
#include <map>

#include "TMath.h"
#include "Math/ProbFuncMathCore.h"
#include "Math/QuantFuncMathCore.h"


class AsymptoticCLsTool {
private:
    double targetCLs_;
    double precision_;
    bool doTilde_;
    int direction_;
    
    ClassDef(AsymptoticCLsTool, 1)
public:
    AsymptoticCLsTool(const double &targetCLs, const double &precision = 0.005, const bool &doTilde = true) :
        targetCLs_(targetCLs), precision_(precision), doTilde_(doTilde), direction_(1) {}
    
    double calcCLs(const double &qmu_tilde, const double &sigma, const double &mu);
    double calcDerCLs(const double &qmu, const double &sigma, const double &mu);
    double calcPb(const double &qmu, const double &sigma, const double &mu);
    double calcPmu(const double &qmu, const double &sigma, const double &mu);
    double getQmu95(const double &sigma, const double &mu, const int &itermax=200);
    double getQmu95_brute(const double &sigma, const double &mu, const double &vmax=20.);
    double findCrossing(const double &sigma_obs, const double &sigma, const double &muhat);
    double getSigma(const double &mu, const double &mu_hat, const double &qmu);
    
    const double& getTargetCLs() const { return targetCLs_; }
    const int& getDircetion() const { return direction_;}
    void setTargetCLs(double targetCLs){ targetCLs_ = targetCLs;}
    void setDirection(int direction){ direction_ = direction;}
};

#endif // ASYMPTOTIC_CLS_TOOL