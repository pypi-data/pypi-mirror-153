#include "libgeopack.h"


double GetDipoleTilt() {
	/* Returns the dipole tilt angle in radians*/
	return GP1.PSI;
}

CustParam CustP;
const float Re = 6371.2;
TSD TSData = {.n = 0};
char DataFile[256];

void LoadTSData() {
	printf("Reading Model Data\n");
	FILE *f = fopen(DataFile,"rb");
	if (f == NULL) {
		printf("Full file path: %s",DataFile);
		printf("File open failed!\n");
	}
	int n;
	fread(&n,sizeof(int),1,f);
	TSData.n = n;
	TSData.Date = (int *) malloc(sizeof(int)*TSData.n);
	fread(TSData.Date,sizeof(int),TSData.n,f);
	TSData.ut = (float *) malloc(sizeof(float)*TSData.n);
	fread(TSData.ut,sizeof(float),TSData.n,f);
	TSData.Year = (int *) malloc(sizeof(int)*TSData.n);
	fread(TSData.Year,sizeof(int),TSData.n,f);
	TSData.DayNo = (int *) malloc(sizeof(int)*TSData.n);
	fread(TSData.DayNo,sizeof(int),TSData.n,f);
	TSData.Hr = (int *) malloc(sizeof(int)*TSData.n);
	fread(TSData.Hr,sizeof(int),TSData.n,f);
	TSData.Mn = (int *) malloc(sizeof(int)*TSData.n);
	fread(TSData.Mn,sizeof(int),TSData.n,f);
	TSData.Bx = (float *) malloc(sizeof(float)*TSData.n);
	fread(TSData.Bx,sizeof(float),TSData.n,f);
	TSData.By = (float *) malloc(sizeof(float)*TSData.n);
	fread(TSData.By,sizeof(float),TSData.n,f);
	TSData.Bz = (float *) malloc(sizeof(float)*TSData.n);
	fread(TSData.Bz,sizeof(float),TSData.n,f);
	TSData.Vx = (float *) malloc(sizeof(float)*TSData.n);
	fread(TSData.Vx,sizeof(float),TSData.n,f);
	TSData.Vy = (float *) malloc(sizeof(float)*TSData.n);
	fread(TSData.Vy,sizeof(float),TSData.n,f);
	TSData.Vz = (float *) malloc(sizeof(float)*TSData.n);
	fread(TSData.Vz,sizeof(float),TSData.n,f);	
	TSData.Den = (float *) malloc(sizeof(float)*TSData.n);
	fread(TSData.Den,sizeof(float),TSData.n,f);
	TSData.Temp = (float *) malloc(sizeof(float)*TSData.n);
	fread(TSData.Temp,sizeof(float),TSData.n,f);
	TSData.SymH = (float *) malloc(sizeof(float)*TSData.n);
	fread(TSData.SymH,sizeof(float),TSData.n,f);
	TSData.IMFFlag = (int *) malloc(sizeof(int)*TSData.n);
	fread(TSData.IMFFlag,sizeof(int),TSData.n,f);
	TSData.ISWFlag = (int *) malloc(sizeof(int)*TSData.n);
	fread(TSData.ISWFlag,sizeof(int),TSData.n,f);
	TSData.Tilt = (float *) malloc(sizeof(float)*TSData.n);
	fread(TSData.Tilt,sizeof(float),TSData.n,f);
	TSData.Pdyn = (float *) malloc(sizeof(float)*TSData.n);
	fread(TSData.Pdyn,sizeof(float),TSData.n,f);
	TSData.W1 = (float *) malloc(sizeof(float)*TSData.n);
	fread(TSData.W1,sizeof(float),TSData.n,f);	
	TSData.W2 = (float *) malloc(sizeof(float)*TSData.n);
	fread(TSData.W2,sizeof(float),TSData.n,f);
	TSData.W3 = (float *) malloc(sizeof(float)*TSData.n);
	fread(TSData.W3,sizeof(float),TSData.n,f);
	TSData.W4 = (float *) malloc(sizeof(float)*TSData.n);
	fread(TSData.W4,sizeof(float),TSData.n,f);
	TSData.W5 = (float *) malloc(sizeof(float)*TSData.n);
	fread(TSData.W5,sizeof(float),TSData.n,f);
	TSData.W6 = (float *) malloc(sizeof(float)*TSData.n);
	fread(TSData.W6,sizeof(float),TSData.n,f);
	TSData.G1 = (float *) malloc(sizeof(float)*TSData.n);
	fread(TSData.G1,sizeof(float),TSData.n,f);	
	TSData.G2 = (float *) malloc(sizeof(float)*TSData.n);
	fread(TSData.G2,sizeof(float),TSData.n,f);	
	TSData.Kp = (float *) malloc(sizeof(float)*TSData.n);
	fread(TSData.Kp,sizeof(float),TSData.n,f);		
	fclose(f);
	
	PopulateMonthInds();
	printf("Done\n");
}

void PopulateMonthInds() {
	int minYr, minMn, maxYr, maxMn, tmp,tmpYr,tmpMn;
	minYr = TSData.Year[0];
	minMn = (TSData.Date[0] % 10000)/100;
	maxYr = TSData.Year[TSData.n-1];
	maxMn = (TSData.Date[TSData.n-1] % 10000)/100;	
	
	TSData.minYr = minYr;
	TSData.minMn = minMn;
	TSData.nMonth = 12*(maxYr-minYr) + maxMn - minMn + 1;
	TSData.MonthInds = (int *) malloc(sizeof(int)*TSData.nMonth);
	
	tmpYr = minYr;
	tmpMn = minMn;
	
	int i, j, p = 0;
	for (i=0;i<TSData.nMonth;i++) {
		tmp = tmpYr*10000 + tmpMn*100;
		for (j=p;j<TSData.n;j++) {
			if (TSData.Date[j] >= tmp) {
				p = j;
				TSData.MonthInds[i] = j;
				tmpMn++;
				if (tmpMn > 12) {
					tmpMn = 1;
					tmpYr++;
				}
				break;
			}
		}
	}		
}

int MonthStartInd(int Date) {
	int yr, mn, ind;
	yr = Date / 10000;
	mn = (Date % 10000)/100;
	ind = (yr - TSData.minYr)*12 + mn - TSData.minMn;

	if (ind >= TSData.nMonth){
		ind = TSData.nMonth-1;
	}
	return TSData.MonthInds[ind];
}

void FreeTSData() {
	if (TSData.n > 0) {
		free(TSData.Date);
		free(TSData.ut);
		free(TSData.Year);
		free(TSData.DayNo);
		free(TSData.Hr);
		free(TSData.Mn);
		free(TSData.Bx);
		free(TSData.By);
		free(TSData.Bz);
		free(TSData.Vx);
		free(TSData.Vy);
		free(TSData.Vz);
		free(TSData.Den);
		free(TSData.Temp);
		free(TSData.SymH);
		free(TSData.IMFFlag);
		free(TSData.ISWFlag);
		free(TSData.Tilt);
		free(TSData.Pdyn);
		free(TSData.W1);
		free(TSData.W2);
		free(TSData.W3);
		free(TSData.W4);
		free(TSData.W5);
		free(TSData.W6);
		free(TSData.G1);
		free(TSData.G2);
		free(TSData.Kp);
		free(TSData.MonthInds);
		TSData.n = 0;
	}
}

double InterpParam(float *x, int Date, float ut) {
	/*First get the start ind for searching for this date*/
	int ind = MonthStartInd(Date);
	int i, i0, i1;
	/*now start search for nearest two indices*/
	if ((TSData.Date[ind] > Date) || ((TSData.Date[ind] == Date) && (TSData.ut[ind] > ut))){
		//if the index corresponds to a time after the current time then set i0 to the time index before
		i0 = ind - 1;
		if (i0 < 0) {
			i0 = 0;
		}
		i1 = i0+1;
	} else {
		i = ind;
		while ((i < TSData.n - 1) && ((TSData.Date[i] < Date) || ((TSData.Date[i] == Date) && (TSData.ut[i] <= ut)))) {
			i++;
		}
		i0 = i-1;
		i1 = i;
	}	

	/*now to calculate time differences between two points and the first point witht he requested time*/
	float dt, dtp;
	dt = TimeDifference(TSData.Date[i0],TSData.ut[i0],TSData.Date[i1],TSData.ut[i1]);
	dtp = TimeDifference(TSData.Date[i0],TSData.ut[i0],Date,ut);
	/*now the linear interpolation*/
	float out, m, c;
	m = (x[i1]-x[i0])/dt;
	c = x[i0];
	out = m*dtp + c;
	return (double) out;
}

void GetModelParams(int Date, float ut, const char *Model, int *iopt, double *parmod, float *tilt, float *Vx, float *Vy, float *Vz) {
	/*Dipole tilt*/
	tilt[0] = InterpParam(TSData.Tilt,Date,ut);

	/*Vx, Vy, Vz*/
	Vx[0] = InterpParam(TSData.Vx,Date,ut);
	Vy[0] = InterpParam(TSData.Vy,Date,ut);
	Vz[0] = InterpParam(TSData.Vz,Date,ut);	
	/*The easiest one is T89 - just need Kp*/
    if ((strcmp(Model,"T89") == 0) || (strcmp(Model,"T89c") == 0)) {
		iopt[0] = (int) InterpParam(TSData.Kp,Date,ut) + 1;
		if (iopt[0] > 7) {
			iopt[0] = 7;
		} else if (iopt[0] < 1) {
			iopt[0] = 1;
		}
//		return;
	/* Then T96 is Pdyn, Dst (SymH in this case), By, Bz */
	} else if ((strcmp(Model,"T96") == 0) || (strcmp(Model,"T96c") == 0)) {
		parmod[0] = InterpParam(TSData.Pdyn,Date,ut);
		parmod[1] = InterpParam(TSData.SymH,Date,ut);
		parmod[2] = InterpParam(TSData.By,Date,ut);
		parmod[3] = InterpParam(TSData.Bz,Date,ut);
//		return;
	/* Next T01 which uses: Pdyn, Dst, By, Bz, G1, G2*/
	} else if ((strcmp(Model,"T01") == 0) || (strcmp(Model,"T01c") == 0)) {
		parmod[0] = InterpParam(TSData.Pdyn,Date,ut);
		parmod[1] = InterpParam(TSData.SymH,Date,ut);
		parmod[2] = InterpParam(TSData.By,Date,ut);
		parmod[3] = InterpParam(TSData.Bz,Date,ut);
		parmod[4] = InterpParam(TSData.G1,Date,ut);
		parmod[5] = InterpParam(TSData.G2,Date,ut);
//		return;
	/*TS05: Pdyn, Dst, By, Bz, W1, W2, W3, W4, W5, W6*/
	} else if ((strcmp(Model,"TS05") == 0) || (strcmp(Model,"TS05c") == 0)) {
		parmod[0] = InterpParam(TSData.Pdyn,Date,ut);
		parmod[1] = InterpParam(TSData.SymH,Date,ut);
		parmod[2] = InterpParam(TSData.By,Date,ut);
		parmod[3] = InterpParam(TSData.Bz,Date,ut);
		parmod[4] = InterpParam(TSData.W1,Date,ut);
		parmod[5] = InterpParam(TSData.W2,Date,ut);		
		parmod[6] = InterpParam(TSData.W3,Date,ut);
		parmod[7] = InterpParam(TSData.W4,Date,ut);
		parmod[8] = InterpParam(TSData.W5,Date,ut);
		parmod[9] = InterpParam(TSData.W6,Date,ut);	
//		return;
	} 
	if (strchr(Model,'c') != NULL) {
		//In this bit we have chosen a custom model, so will use the custom params stored in CustP
		//So, setting CustP needs to be done first!
		if (!isnan(CustP.tilt)) {
			//if we set CustP.tilt = NaN then we use the default interpolated value
			//otherwise we set it to a specific value
			tilt[0] = CustP.tilt;
		}
		iopt[0] = CustP.iopt;
		Vx[0] = CustP.Vx;
		Vy[0] = CustP.Vy;
		Vz[0] = CustP.Vz;
		int i;
		for (i=0;i<10;i++) {
			parmod[i] = CustP.parmod[i];
		}
	}
}


void DummyFunc(int iopt, double *parmod, double ps, double x, double y, double z, double *bx, double *by, double *bz) {
	bx[0] = 0.0;
	by[0] = 0.0;
	bz[0] = 0.0;
	return;
}

void SetCustParam(int iopt, double *parmod, float tilt, float Vx, float Vy, float Vz) {
	CustP.iopt = iopt;
	int i;
	for (i=0;i<10;i++) {
		CustP.parmod[i] = parmod[i];
	}
	CustP.tilt = tilt;
	CustP.Vx = Vx;
	CustP.Vy = Vy;
	CustP.Vz = Vz;
}


void Init(const char *filename, const char *igrffile) {
	strcpy(DataFile,filename);
	if (TSData.n == 0) {
		LoadTSData();	
	}
	ReadIGRFParameters(igrffile);
}

void GetGeopackParams(double *gp0, double *gp1) {
	int i;
	
	gp0[0] = GP1.ST0;
	gp0[1] = GP1.CT0;
	gp0[2] = GP1.SL0;
	gp0[3] = GP1.CL0;
	gp0[4] = GP1.CTCL;
	gp0[5] = GP1.STCL;
	gp0[6] = GP1.CTSL;
	gp0[7] = GP1.STSL;
	gp0[8] = GP1.SFI;
	gp0[1] = GP1.CFI;
	gp0[10] = GP1.SPS;
	gp0[11] = GP1.CPS;
	gp0[12] = GP1.DS3;
	gp0[13] = GP1.CGST;
	gp0[14] = GP1.SGST;
	gp0[15] = GP1.PSI;
	gp0[16] = GP1.A11;
	gp0[17] = GP1.A21;
	gp0[18] = GP1.A31;
	gp0[19] = GP1.A12;
	gp0[20] = GP1.A22;
	gp0[21] = GP1.A32;
	gp0[22] = GP1.A13;
	gp0[23] = GP1.A23;
	gp0[24] = GP1.A33;
	gp0[25] = GP1.E11;
	gp0[26] = GP1.E21;
	gp0[27] = GP1.E31;
	gp0[28] = GP1.E12;
	gp0[29] = GP1.E22;
	gp0[30] = GP1.E32;
	gp0[31] = GP1.E13;
	gp0[32] = GP1.E23;
	gp0[33] = GP1.E33;
 
	for (i=0;i<105;i++) {
		gp1[i] = IGRFCurr.g[i];
		gp1[i+105] = IGRFCurr.h[i];
		gp1[i+210] = IGRFCurr.rec[i];
	}
 

}


void SetGeopackParams(double *gp0, double *gp1) {
	int i;
	
	GP1.ST0 = gp0[0];
	GP1.CT0 = gp0[1];
	GP1.SL0 = gp0[2];
	GP1.CL0 = gp0[3];
	GP1.CTCL = gp0[4];
	GP1.STCL = gp0[5];
	GP1.CTSL = gp0[6];
	GP1.STSL = gp0[7];
	GP1.SFI = gp0[8];
	GP1.CFI = gp0[9];
	GP1.SPS = gp0[10];
	GP1.CPS = gp0[11];
	GP1.DS3 = gp0[12];
	GP1.CGST = gp0[13];
	GP1.SGST = gp0[14];
	GP1.PSI = gp0[15];
	GP1.A11 = gp0[16];
	GP1.A21 = gp0[17];
	GP1.A31 = gp0[18];
	GP1.A12 = gp0[19];
	GP1.A22 = gp0[20];
	GP1.A32 = gp0[21];
	GP1.A13 = gp0[22];
	GP1.A23 = gp0[23];
	GP1.A33 = gp0[24];
	GP1.E11 = gp0[25];
	GP1.E21 = gp0[26];
	GP1.E31 = gp0[27];
	GP1.E12 = gp0[28];
	GP1.E22 = gp0[29];
	GP1.E32 = gp0[30];
	GP1.E13 = gp0[31];
	GP1.E23 = gp0[32];
	GP1.E33 = gp0[33];
 
	for (i=0;i<105;i++) {
		IGRFCurr.g[i] = gp1[i];
		IGRFCurr.h[i] = gp1[i+105];
		IGRFCurr.rec[i] = gp1[i+210];
	}
 

}
