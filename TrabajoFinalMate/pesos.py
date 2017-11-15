import numpy as np

class p:
    def __init__(self,rp):
        self.rp = rp
        np.seterr(divide='ignore', invalid='ignore')

    def hallarDesv(self,acciones):
        rp = self.rp
        totalLog = 0
        L=0
        covList=[]
        for x in reversed(range(1,len(acciones))):
            n = acciones[x]
            nant = acciones[x-1]
            cov = np.log((n/nant))
            covList.append(cov)
            totalLog += cov
            L+=1
        r = totalLog/L
        #print ("r",r.shape)
        cov = np.cov(np.transpose(covList))
        #print("cov",cov.shape)
        covinverse = np.linalg.inv(cov)
        #print("covinverse", covinverse.shape)
        unos = np.ones((cov.shape[0],1))
        #print(np.transpose(unos).shape)
        #print("unos",unos.shape)
        a = np.dot(np.dot(np.transpose(r),covinverse),r)
        b = np.dot(np.dot(np.transpose(r),covinverse),unos)
        b=b[0]
        c = np.dot(np.dot(np.transpose(unos),covinverse),unos)
        c=c[0][0]
        d = (a*c)-np.power(b,2)
        #print("a",a)
        #print("b",b)
        #print("c",c)
        #print("d",d)
        ff=((c/d)*np.dot(covinverse,r))
        ff=np.reshape(ff,(cov.shape[0],1))
        #print (ff.shape)
        fs = ((b/d)*np.dot(covinverse,unos))
        #print(fs.shape)
        h = (ff-fs)*rp
        #print("h",h.shape)
        sf = ((-b)/d)*np.dot(covinverse,r)
        sf = np.reshape(sf, (cov.shape[0], 1))
        #print(sf.shape)
        ss = (a/d)*np.dot(covinverse,unos)
        k = sf + ss
        w = h+k
        #print ("w",w.shape)
        devf = np.dot(np.transpose(w),cov)
        devint = np.dot(devf,w)
        desv = np.sqrt(devint)
        return desv







