library(fitdistrplus)


fileUri = "C:/Users/Tom/Documents/Computing Science/ADS/rawdata/runtimes.csv"
input <- read.csv(file=fileUri,head=TRUE,sep=";")


df = data.frame(matrix(nrow = 14, ncol = 8))
rownames(df) <- colnames(input)
colnames(df) <- c("lognormal", "gamma", "normal", "weibull", "biclognormal", "bicgamma", "bicnormal", "bicweibull")

gEst = data.frame(matrix(nrow=14, ncol=2))
rownames(gEst) <- colnames(input)
colnames(gEst) <- c("shape", "rate")

for(stop in colnames(input)){
  col <- input[,stop]
  
  fg <- fitdist(col, "gamma")
  fln <- fitdist(col, "lnorm")
  fn <- fitdist(col, "norm")
  fb <- fitdist(col, "weibull")
  
  gEst[stop, "shape"] = fg$estimate[["shape"]]
  gEst[stop, "rate"] = fg$estimate[["rate"]]
  
  
  stats <- gofstat(list(fg, fln, fn, fb), fitnames = c("lognormal", "gamma", "normal", "weibull"))
  ksTest <- stats[["ks"]]
  asd <- ksTest[["normal"]]
  BIC <- stats[["bic"]]
  df[stop, "lognormal"] <- ksTest[["lognormal"]]
  df[stop, "gamma"] <- ksTest[["gamma"]]
  df[stop, "normal"] <- ksTest[["normal"]]
  df[stop, "weibull"] <- ksTest[["weibull"]]
  df[stop, "biclognormal"] <- BIC[["lognormal"]]
  df[stop, "bicgamma"] <- BIC[["gamma"]]
  df[stop, "bicnormal"] <- BIC[["normal"]]
  df[stop, "bicweibull"] <- BIC[["weibull"]]
}

#outUrl <- "C:/Users/Tom/Documents/Computing Science/ADS/processeddata/runtimeAnalysis.csv"
outUrl <- "C:/Users/Tom/Documents/Computing Science/ADS/processeddata/gammaParameters.csv"
#write.csv(gEst, outUrl)

#mea <- mean(input[,"Graadt.van.Roggenweg"])

set.seed(101)     # unkonwn distribution parameters

fit <- fitdistr(input$Graadt.van.Roggenweg, densfun="gamma")  # we assume my_data ~ Normal(?,?)

hist(input$Graadt.van.Roggenweg, pch=20, breaks=25, prob=TRUE, main="")
curve(dgamma(x, fit$estimate[1], fit$estimate[2]), col="red", lwd=2, add=T)