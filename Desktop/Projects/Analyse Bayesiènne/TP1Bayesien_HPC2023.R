# Correction TP1 HPC-BigData : Analyse Bayesienne - Theorie de la decision 


#1-Initialisation

install.packages("rootSolve",dep=T)
library(rootSolve)

n = 150
x = 6


# 2- Phase d'elicitation du prior

model = function(x,pa,qa,pb,qb){
c(F1=pa-pbeta(qa,x[1],x[2]),
  F2=pb-pbeta(qb,x[1],x[2]))}

sol = multiroot(f=model,start=c(1,10),positive=T,pa=0.05,qa=0.01,pb=0.90,qb=0.05)

p=sol$root[1]
q=sol$root[2]


# 3- Elaboration du posterior

x11(wi=10,he=8)
axe_x=seq(0,0.2,.0001)
plot(axe_x,dbeta(axe_x,x+p,n-x+q),xaxs="i",yaxs="i",type="l",lwd=3,ylab="DENSITE",xlab=expression(theta))
lines(axe_x,dbeta(axe_x,p,q),col="red",lwd=3)
legend(0.1,20,legend=c("POSTERIOR","PRIOR"),text.col=c("black","red"),bty="n")


# 4- Distribution predictive a posteriori

polya = function(y,h,p,q,n,x) {choose(h,y)*beta(y+x+p,h-y+n-x+q)/beta(x+p,n-x+q)}

x11(wi=10,he=8)
par(mfrow=c(2,2))
y = 0:10
for (h in c(5,10,20,30)){
plot(y,polya(y,h,p,q,n,x),type="h",lwd=6,main=paste("h=",h,"ans"),xlab="NB ANNEES AVEC AVALANCHE",ylab="PROBABILITE",ylim=c(0,1),yaxs="i")}


# 5- Outil d'aide a la prise de decision

h       = seq(1,20,0.1)
p_h     = 1-polya(0,h,p,q,n,x)

x11(wi=10,he=8)
plot(h,(1-p_h)/p_h,type="l",xlab="h",ylab="C1/C2",xaxs="i",yaxs="i",ylim=c(1,25),main="Avec Prior beta")
text(3,2,"a1",cex=2)
text(10,10,"a2",cex=2)
abline(6,0)

# --> decision a2


# 6- Epilogue

# Refaire avec prior non informatif de Jeffreys :

p = 1/2
q = 1/2

h       = seq(1,20,0.1)
p_h     = 1-polya(0,h,p,q,n,x)

x11(wi=10,he=8)
plot(h,(1-p_h)/p_h,type="l",xlab="h",ylab="C1/C2",xaxs="i",yaxs="i",ylim=c(1,25),main="Avec Prior de Jeffreys")
text(3,2,"a1",cex=2)
text(10,10,"a2",cex=2)
abline(6,0)

# la conclusion est la meme : decision a2, il ne fallait pas construire.
