#include "AsymptoticCLsTool.h"

ClassImp(AsymptoticCLsTool)
    
double AsymptoticCLsTool::getSigma(const double &mu, const double &mu_hat, const double &qmu)
{
    double sigma;
    if (mu * direction_ < mu_hat)
        sigma = fabs(mu - mu_hat)/sqrt(qmu);
    else if ((mu_hat < 0) and doTilde_)
        sigma = sqrt( mu * mu - 2 * mu * mu_hat * direction_)/sqrt(qmu);
    else
        sigma = (mu - mu_hat) * direction_ / sqrt(qmu);
    return sigma;
}
    
double AsymptoticCLsTool::findCrossing(const double &sigma_obs, const double &sigma, const double &muhat)
{
    double mu_guess = muhat + ROOT::Math::gaussian_quantile(1 - targetCLs_, 1) * sigma_obs * direction_;
    //std::cout<<"mu guess: "<<mu_guess<<std::endl;
    int nrItr = 0;
    int nrDamping = 1;

    std::map<double, double> guess_to_corr;
    double damping_factor = 1.0;
    double mu_pre = mu_guess - 10 * mu_guess * precision_;
    
    while (fabs(mu_guess - mu_pre) > direction_ * mu_guess * precision_)
    {
        double sigma_obs_extrap = sigma_obs;
        double eps = 0;

        mu_pre = mu_guess;

        double qmu95 = getQmu95(sigma, mu_guess);
        double qmu;
        if (muhat < 0 && doTilde_)
            qmu = (1. / (sigma_obs_extrap * sigma_obs_extrap)) * (mu_guess * mu_guess - 2 * mu_guess * muhat);
        else
            qmu = (1. / (sigma_obs_extrap * sigma_obs_extrap)) * ((mu_guess - muhat) * (mu_guess - muhat));

        double dqmu_dmu = 2 * (mu_guess - muhat) / (sigma_obs_extrap * sigma_obs_extrap) - 2 * qmu * eps;

        double corr = damping_factor * (qmu - qmu95) / dqmu_dmu;
        for (std::map<double, double>::iterator itr = guess_to_corr.begin(); itr != guess_to_corr.end(); itr++)
        {
            if (fabs(itr->first - mu_guess) < direction_ * mu_guess * precision_)
            {
                damping_factor *= 0.8;
                if (nrDamping++ > 10)
                {
                    nrDamping = 1;
                    damping_factor = 1.0;
                }
                corr *= damping_factor;
                break;
            }
        }
        guess_to_corr[mu_guess] = corr;

        mu_guess = mu_guess - corr;
        nrItr++;
        if (nrItr > 100)
        {
            std::cout << "Infinite loop detected in findCrossing. Please intervene." << std::endl;
            return 0;
        }
    }
    
    return mu_guess;
}

double AsymptoticCLsTool::calcPb(const double &qmu, const double &sigma, const double &mu)
{
    double pb;

    if (qmu < mu * mu / (sigma * sigma) || !doTilde_)
        pb = 1 - ROOT::Math::gaussian_cdf(fabs(mu / sigma) - sqrt(qmu));
    else
        pb = 1 - ROOT::Math::gaussian_cdf((mu * mu / (sigma * sigma) - qmu) / (2 * fabs(mu / sigma)));
    //std::cout<<"INFO: pb:"<<pb<<std::endl;
    return pb;
}

double AsymptoticCLsTool::calcPmu(const double &qmu, const double &sigma, const double &mu)
{
    double pmu;

    if (qmu < mu * mu / (sigma * sigma) || !doTilde_)
        pmu = 1 - ROOT::Math::gaussian_cdf(sqrt(qmu));
    else
        pmu = 1 - ROOT::Math::gaussian_cdf((qmu + mu * mu / (sigma * sigma)) / (2 * fabs(mu / sigma)));
    //std::cout<<"INFO: pmu"<<pmu<<std::endl;
    return pmu;
}

double AsymptoticCLsTool::calcCLs(const double &qmu_tilde, const double &sigma, const double &mu)
{
    double pmu = calcPmu(qmu_tilde, sigma, mu);
    double pb = calcPb(qmu_tilde, sigma, mu);
    if (pb == 1) 
        return 0.5;
    double CLs = pmu / (1 - pb);
    //std::cout<<"INFO: CLs"<<CLs<<std::endl;
    return CLs;
}

double AsymptoticCLsTool::calcDerCLs(const double &qmu, const double &sigma, const double &mu)
{
    double dpmu_dq = 0;
    double d1mpb_dq = 0;

    double mu2 = mu * mu;
    double sigma2 = sigma * sigma;

    if (qmu < mu2 / sigma2)
    {
        double zmu = sqrt(qmu);
        dpmu_dq = -1. / (2 * sqrt(qmu * 2 * TMath::Pi())) * exp(-zmu * zmu / 2);

        double zb = fabs(mu / sigma) - sqrt(qmu);
        d1mpb_dq = -1. / (2 * sqrt(qmu * 2 * TMath::Pi())) * exp(-zb * zb / 2);
        //std::cout<<"DEBUG: Case 1, qmu:"<<qmu<<" zb:"<<zb<<std::endl;
    }
    else
    {
        double alpha = 2 * fabs(mu / sigma);
        double zmu = (qmu + mu2 / sigma2) / alpha;
        dpmu_dq = -1. / alpha * 1. / (sqrt(2 * TMath::Pi())) * exp(-zmu * zmu / 2);

        double zb = (mu2 / sigma2 - qmu) / alpha;
        d1mpb_dq = -1. / alpha * 1. / (sqrt(2 * TMath::Pi())) * exp(-zb * zb / 2);
        //std::cout<<"DEBUG: Case 2, alpha:"<<alpha<<" zb:"<<zb<<std::endl;
    }

    double pb = calcPb(qmu, sigma, mu);
    double derCLs = dpmu_dq / (1 - pb) - calcCLs(qmu, sigma, mu) / (1 - pb) * d1mpb_dq;
    //std::cout<<"INFO: derCLs:"<<derCLs<<" dpmu_dq:"<<dpmu_dq<<" pb:"<<pb<<" d1mpb_dq:"<<d1mpb_dq<<std::endl;
    return derCLs;
}



double AsymptoticCLsTool::getQmu95(const double &sigma, const double &mu, const int &itermax)
{
    double qmu95 = 0;
    //no sane man would venture this far down into |mu/sigma|
    double target_N = ROOT::Math::gaussian_quantile(1 - targetCLs_, 1);
    if (fabs(mu / sigma) < 0.25 * target_N)
    {
        qmu95 = 5.83 / target_N;
    }
    else
    {
        std::map<double, double> guess_to_corr;
        double qmu95_guess = pow(ROOT::Math::gaussian_quantile(1 - targetCLs_, 1), 2);
        int nrItr = 0;
        int nrDamping = 1;
        double damping_factor = 1.0;
        double qmu95_pre = qmu95_guess - 10 * 2 * qmu95_guess * precision_;
        while (fabs(qmu95_guess - qmu95_pre) > 2 * qmu95_guess * precision_)
        {
            qmu95_pre = qmu95_guess;

            double corr = damping_factor * (calcCLs(qmu95_guess, sigma, mu) - targetCLs_) / calcDerCLs(qmu95_guess, sigma, mu);
            for (std::map<double, double>::iterator itr = guess_to_corr.begin(); itr != guess_to_corr.end(); itr++)
            {
                if (fabs(itr->first - qmu95_guess) < 2 * qmu95_guess * precision_)
                {
                    damping_factor *= 0.8;
                    if (nrDamping++ > 10)
                    {
                        nrDamping = 1;
                        damping_factor = 1.0;
                    }
                    corr *= damping_factor;
                }
            }

            guess_to_corr[qmu95_guess] = corr;
            qmu95_guess = qmu95_guess - corr;

            nrItr++;
            if (nrItr > itermax)
            {
                std::cout << "Infinite loop detected in getQmu95. Please intervene." << std::endl;
                exit(1);
            }
        }
        qmu95 = qmu95_guess;
    }

    if (qmu95 != qmu95)
        qmu95 = getQmu95_brute(sigma, mu);
    //std::cout<<"INFO: qmu95:"<<qmu95<<std::endl;
    return qmu95;
}

double AsymptoticCLsTool::getQmu95_brute(const double &sigma, const double &mu, const double &vmax)
{
    double step_size = 0.001;
    double start = step_size;

    if (mu / sigma > 0.2) 
        start = 0;
    for (double qmu = start; qmu < vmax; qmu += step_size)
    {
        double CLs = calcCLs(qmu, sigma, mu);
        if (CLs < targetCLs_)
            return qmu;
    }
    
    return vmax;
}