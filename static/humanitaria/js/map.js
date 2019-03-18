function map(embarazadas, dengue) {
    var emb = L.layerGroup(embarazadas);
    var den = L.layerGroup(dengue);


    var map = L.map('map', {
    center: [19.419444,  -99.145556],
    zoom: 5,
        layers: [emb, den]
    });


    var overlays = {
        "Embarazadas": emb,
        "Dengue": den
}
    ;

    L.control.layers(overlays).addTo(map);
}