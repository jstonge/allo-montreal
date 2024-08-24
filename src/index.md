# Allô Montréal
## Montreal 56 electoral counties

```js
const metadata = FileAttachment("metadata.parquet").parquet();
const mtl_topo = FileAttachment("mtl_topo.json").json();
```

```js
const districts_mesh = topojson.mesh(mtl_topo, mtl_topo.objects.districts)
const districts = topojson.feature(mtl_topo, mtl_topo.objects.districts).features
```

```js
// create inputs based on time
const yearSelect = view(Inputs.radio([2011, 2016], {label: "Population Size:", value: 2011}))
```

```js
const metadata_f = [...metadata].filter(d=>d.year == parseInt(yearSelect))
```

```js
// create lookup to map districts => popSize
const pop_arr = new Map(metadata_f.map(({arrondissement, population}) => [arrondissement, population]))
```

```js
Plot.plot({
    width: 1200,
    height: 800,
    projection: {
        domain: d3.geoCircle().center([-73.711, 45.56]).radius(0.16)(),
        type: "reflect-y",
    },
    color: {
        legend: true,
        scheme: "spectral",
        label: "population size",
        type: "linear",
        domain: [0, d3.max(metadata, d=>d.population)],
        width: 400
        },
    marks: [
        // Plot.geo(mtl, { strokeWidth: 0.1 }),
        // Plot.geo(mtl_hydro, {fill: "lightblue"}),
        Plot.geo(districts_mesh),
        Plot.geo(
            districts,
            { fill: (d) => pop_arr.get(d.properties.arrondissement) }
        ),
        Plot.text(districts, Plot.centroid({
            text: (d) => d.properties.nom, fill: "currentColor", stroke: "white"
        }))
    ]
})
```

```js
Inputs.table(metadata)
```