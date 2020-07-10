//Globe
require([
    "esri/Map",
    "esri/views/SceneView",
    "esri/layers/TileLayer",
    "esri/Basemap",
    "esri/geometry/Mesh"
  ], function (Map, SceneView, TileLayer, Basemap, Mesh) {

    const R=6358137;
    const offset=400000;

    const basemap = new Basemap({
      baseLayers: [
        new TileLayer({
          url: "https://tiles.arcgis.com/tiles/nGt4QxSblgDfeJn9/arcgis/rest/services/terrain_with_heavy_bathymetry/MapServer"
        })
      ]
    });

    const map = new Map({
      basemap: basemap
    });

    const view = new SceneView({
      container: "viewDiv",
      map: map,
      constraints: {
        altitude: {
          min: 3000000,
          max: 18000000
        }
      }
    });

    const cloudsSphere=Mesh.createSphere(new Point({
      x:0,y:-90,z:-(2*R+offset)
    }), {
      size: 2*(R+offset),
      material:{
        colorTexture: 'clouds.png',
        doubleSided:false
      },
      densificationFactor:6
    });

    cloudsSphere.components[0].shading="flat";
    const clouds = new Graphic({
      geometry: cloudsSphere,
      symbol: {
        type: "mesh-3d",
        symbolLayers: [{ type: "fill" }]
      }
    });

    view.graphics.add(clouds); 
  });
//Pop-Up