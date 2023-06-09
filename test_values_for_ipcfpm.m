clc
clear
availableResourcesInFed = [409, 696, 90; 
     409, 696, 90; 
     409, 696, 90; 
     409, 696, 90; 
     409, 696, 90; 
     409, 696, 90];

costsOfCPsInFed = [0.03, 0.06, 0.12, 0.24; 
                    0.045, 0.091, 0.182, 0.364; 
                    0.048, 0.096, 0.192, 0.384; 
                    0.033, 0.065, 0.13, 0.26;
                    0.055, 0.111, 0.222, 0.444; 
                    0.04, 0.08, 0.16, 0.32];

vmInfo =  [1., 1.7, 0.22, 0.12;
 2., 3.75, 0.48, 0.24;
 4., 7.5, 0.98, 0.48;
 8., 15., 1.99, 0.96];
userRequest = [100 50 200 500];
[x, profit] = ipCfpm(availableResourcesInFed, costsOfCPsInFed, vmInfo, userRequest)