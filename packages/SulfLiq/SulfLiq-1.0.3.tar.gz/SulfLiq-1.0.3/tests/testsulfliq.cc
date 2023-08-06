
/**
   program induces upchuck from SulfLiq class.
   $Id: testsulfliq.cc,v 1.3 2001/05/09 01:50:28 kress Exp $
   Victor Kress
   Started 4/26/01
*/

#include <iostream>
#include <stdio.h>
#include "SulfLiq.h"
#include "NumUtil.h"

int main() {
  int i,n;
  double *comp,sum,temp;
  static const double spectol=1.e-16;

  SulfLiq *sol = new SulfLiq();
  n = sol->getNcomp();
  comp = new double[n];

  std::cout << "TC = ";
  std::cin >> temp;
  sol->setTk(temp+273.15);

  for (i=0,sum=0.;i<n;i++) {
    std::cout << sol->getCompName(i) << ": ";
    std::cin >> comp[i];
    sum+=comp[i];
  }
  for (i=0;i<n;i++) {
    comp[i]/=sum;
  }

  sol->setComps(comp);
  sol->setSpeciateTolerance(spectol);
  sol->printAll();

  std::cout << "\nTK     = " << sol->getTk();
  std::cout << "\nlogfo2 = " << sol->getlogfo2();
  std::cout << "\nlogfs2 = " << sol->getlogfs2();
  std::cout << "\nisStable = " << sol->isStable();
  sol->printAll();

return 0;
}