# Plano de Bacias PCJ 2020-2035

<br>

A Agência das Bacias PCJ mantem um [ArcGIS Server](https://mapas.agenciapcj.org.br/arcgis/rest/services) possibilitando o consumo de dados espaciais.
Visando baixar todos os dados disponíveis, referente ao [Plano de Bacias 2020-2035](https://plano.agencia.baciaspcj.org.br/), em 20.05.2022 acessei todos os dados usando o repositório [ArcGIS REST API](*).

![ArcGIS Server](https://i.imgur.com/ZAKT1bE.png)

O enderenço com os parâmetros, que utilizei, esta apresentado abaixo:

- https://mapas.agenciapcj.org.br/arcgis/rest/services/Planos/PlanoBacias_CRF/FeatureServer/49/query?where=1%3D1&objectIds=1&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&distance=&units=esriSRUnit_Foot&relationParam=&outFields=*&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&outSR=&havingClause=&gdbVersion=&historicMoment=&returnDistinctValues=false&returnIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&multipatchOption=xyFootprint&resultOffset=&resultRecordCount=&returnTrueCurves=false&returnExceededLimitFeatures=false&quantizationParameters=&returnCentroid=false&sqlFormat=none&resultType=&featureEncoding=esriDefault&datumTransformation=&f=geojson

<br>

**Observação:**

Existem três *layers* que não inseri no repositório, visto apresentarem mais de 25mb. a saber:
- inventario florestal 2020 - bacia pcj - poligonos.7z
- uso da terra - poligonos.7z
- área de preservação permanente - poligonos.7z

<br>

-----

### *TODO*

1. ...

<br>

-----

### Referências

- https://ssd.baciaspcj.org.br/api/index.html
