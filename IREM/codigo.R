# Cargar los datos (ajustar el nombre del archivo y la hoja si es necesario)
library(readxl)
sheets=excel_sheets("../../Ejercicios/IREM/base_sim_datos_peso_ord.xlsx")
data <- read_excel("../../Ejercicios/IREM/base_sim_datos_peso_ord.xlsx",sheet = sheets[1])
tabla_pesos <- read_excel("../../Ejercicios/IREM/base_sim_datos_peso_ord.xlsx",sheet = sheets[2])

length(unique(data$zona_id))
length(unique(data$encuestador_id))
#Primero filtramos a las madres que tienen al menos un hijo varón:
data_filtrada <- data[apply(data, 1, function(x) any(x[1:8*4] == "M" & !is.na(x[1:8*4]))), ]
#De la restricción de tomar el hijo más joven, concluímos que el número de niños a 
#considerar es de la longitud de "data_filtrada"
#Usamos la tabla de pesos.
library(dplyr)
tabla_pesos_intervalos <- tabla_pesos %>% 
  select(Month, SD2neg, SD2) %>% 
  rename(Mes = Month, LimiteInferior = SD2neg, LimiteSuperior = SD2)

#Para decidir si un niño está en su peso adecuado como función de su edad en meses
#Seleccionamos de cada madre, el hijo menor. Naturalmente, por el filtro aplicado 
#anteriormente, sabemos que es menor de 5 años, como se requiere
#Requerimos conocer la edad del niño seleccionado (indice_niño), la cual guardamos en edad_niño.
#Así mismo, guardamos su peso en peso_niño para verificar que sea adecuado según su edad,
#el cual mediremos con un intervalo obtenido de la tabla "tabla_pesos_intervalos"
#Si ocurre que el niño está en su peso adecuado, lo consideraremos para el numerador de nuestro índice.
peso_segun_tabla=function(x){
  indice_niño=which.min(x[1:8*4+1])[[1]]
  edad_niño=as.numeric(x[indice_niño*4+1])
  peso_niño=as.numeric(x[indice_niño*4+1+1])
  intervalo_de_peso=tabla_pesos_intervalos[tabla_pesos_intervalos$Mes==edad_niño,2:3]
  return(peso_niño>intervalo_de_peso$LimiteInferior&peso_niño<intervalo_de_peso$LimiteSuperior)
}
#El numerador lo calculamos con la suma de todos los niños que tienen peso adecuado según la tabla de edades
numerador=sum(apply(data_filtrada,1,peso_segun_tabla))
#Así, somos capaces de calcular el valor del índice: 
denominador=nrow(data_filtrada)
numerador/denominador*100

#Ya que entendimos la manera de calcularlo, procederemos a hacerlo por zona y por encuestador.
#Para ello, consideraremos una función que depende de un conjunto de datos, que puede
#ser el conjunto filtrado a una zona específica o por cada encuestador
calculo_indice=function(data){
  denominador=sum(apply(data,1,function(x) any(x[c(1:8*4+1)]<12*5& !is.na(x[c(1:8*4+1)]))))
  numerador=sum(apply(data,1,peso_segun_tabla
  ))
  return(numerador/denominador*100)
}
#De manera sencilla, lo calcularemos para cada zona distinta y para cada encuestador.
#El supuesto de que cada zona se identifica de manera única
#nos permite considerar los datos de cada zona o de cada encuestador como una base idependiente,
#de manera que el cálculo del indicador se puede simplificar.
zona=c()
indice=c()
for(id in unique(data_filtrada$zona_id)){
  data_filtrada_1=data_filtrada[data_filtrada$zona_id==id,]
  zona=append(zona,id)
  indice=append(indice,calculo_indice(data_filtrada_1))
}
por_zona=setNames(as.data.frame(matrix(c(zona,indice),ncol=2,nrow=length(zona),byrow=F)),c("zona_id","indice"))
encuestador=c()
indice=c()
for(id in unique(data_filtrada$encuestador_id)){
  data_filtrada_1=data_filtrada[data_filtrada$encuestador_id==id,]
  encuestador=append(encuestador,id)
  indice=append(indice,calculo_indice(data_filtrada_1))
}
por_encuestador=setNames(as.data.frame(matrix(c(encuestador,indice),ncol=2,nrow=length(encuestador),byrow=F)),c("encuestador_id","indice"))


#Probaremos las siguientes pruebas estadísticas:
m<-aov(indice~zona_id, data=por_zona)
summary(m)
tukey_result <- TukeyHSD(m)
# Ver los resultados del test post-hoc
tukey_result
kruskal_result <- kruskal.test(indice~zona_id, data=por_zona)
kruskal_result
hist(as.numeric(por_zona$indice),xlab = "Índice",ylab = "Frecuencia",main='Histograma de índice por zona')
library(moments)
skewness(as.numeric(por_zona$indice))

skewness(as.numeric(por_encuestador$indice))
kruskal_result <- kruskal.test(indice~encuestador_id, data=por_encuestador)
kruskal_result
