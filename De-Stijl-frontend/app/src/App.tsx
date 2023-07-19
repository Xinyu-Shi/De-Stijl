import './App.css';

import { ThemeProvider } from '@emotion/react';
import { Grid } from '@mui/material';
import { createTheme, responsiveFontSizes } from '@mui/material/styles';
import { useEffect, useState } from 'react';
import ControlPanelElementsList from './components/ControlPanel/ControlPanelElementsList';
import RecommendationsSection from './components/ControlPanel/RecommendationsSection';
import OverviewSection from './components/ControlPanel/OverviewSection';
import ColorSetupSection from './components/ControlPanel/ColorSetupSection';
import DrawingSettingPanel from './components/Drawing/DrawingCanvas';
import { useFabricJSEditor } from 'fabricjs-react';
import { DiscreteSliders } from './components/ControlPanel/DiscreteSliders';
import { fabric } from "fabric";
import { getColorizerRecommendations, get2DPlatteeGeneration } from './API';

import { template1 } from './template1';
import { template2 } from './template2';
import { template3 } from './template3';
import { template4 } from './template4';
import { template5 } from './template5';
import { template5_plus } from './template5_plus';
import { template6 } from './template6';

export interface Element {
  type: "image" | "text" | "shape";
  value: string
  klass?: any;
  id: number;
  coordinates: any;
  colors: string[];
  locked?: boolean;
  selected?: boolean;
  plattee: string[];
  recommendations: string[];
  selectedRecommendation: number;
  svg?: string;
  base64Image: string;
}

function App() {
  const theme = createTheme({});
  const [mainColors, setMainColors] = useState<string[]>(["#4287f5", "#fa3e7a"]);
  const [selected, setSelected] = useState<number>(0);
  const {selectedObjects, editor, onReady } = useFabricJSEditor({ defaultFillColor: 'white' });
  const [themeEffectValue, setThemeEffectValue] = useState<number>(10);
  const [colorQuantityValue, setColorQuantityValue] = useState<number>(2);
  // const [overviewPalette, setoverviewPalette] = useState<string>('data:image/jpeg;base64, R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==');

  const [loading, setLoading] = useState<boolean>(false);
  const [overviewPalette, setoverviewPalette] = useState<string>('');
 
  // const [elements, setElements] = useState<Element[]>([]);

//  const [elements, setElements] = useState<Element[]>([...template1]);

  // const [elements, setElements] = useState<Element[]>([...template2]);

//   const [elements, setElements] = useState<Element[]>([...template3]);

  //  const [elements, setElements] = useState<Element[]>([...template4]);

  // const [elements, setElements] = useState<Element[]>([...template5]);
  const [elements, setElements] = useState<Element[]>([...template5_plus]);
  // const [elements, setElements] = useState<Element[]>([...template6]);

  let objectId: number = 0
  let textValue: number = 1
  let imageValue: number = 1
  let shapeValue: number = 1

  fabric.Object.prototype.objectCaching = false;

  useEffect(() => {
  }, []);

  const load = () => {
    console.log(elements)
    elements.sort((a, b) => (a.id > b.id) ? 1 : ((b.id > a.id) ? -1 : 0))
    elements.forEach((element: Element) => {
      if (element.type == "image") {
        fabric.Image.fromURL(element.base64Image, function (img) {
          img.set({
            name: element.id.toString(),
            left: element.klass.left,
            top: element.klass.top,
            width: element['coordinates']['br']['x'] - element['coordinates']['bl']['x'],
            height: element['coordinates']['br']['y'] - element['coordinates']['tl']['y'],
          })
          editor?.canvas.add(img);
          img.moveTo(element.id)
          editor?.canvas.requestRenderAll();
        })
      }
      else {
        if (!element.svg) return
        fabric.loadSVGFromString(element.svg, function (objects, options) {
          var svg = fabric.util.groupSVGElements(objects, options);

          if (element.type == "text") svg.set({ type: "text" })
          else svg.set({ type: "path" })
          svg.set({
            name: element.id.toString(),
            left: element.klass.left,
            top: element.klass.top,
            scaleX: element.klass.scaleX,
            scaleY: element.klass.scaleY,
          })
          editor?.canvas.add(svg);
          svg.moveTo(element.id)
          editor?.canvas.requestRenderAll();
        })
      }
    })
  }

// To do: sync the old status of the elemnts 
  const getUpdatedElements = (): Element[] => {
    const objects = editor?.canvas.getObjects();
    // console.log(objects)
    // console.log(objectId)
    if (!objects) return []
    const newElements: Element[] = [];

  
    for (let i = 0; i < objects.length; i++) {
      let objectType: "image" | "text" | "shape"
      let objectValue
      if (objects[i].isType('text')) {
        objectType = "text"
        objectValue = "Text " + (textValue++).toString()
      }
      else if (objects[i].get('type') == "circle" || objects[i].get('type') == "rect" || objects[i].get('type') == "path") {
        objectType = "shape"
        objectValue = "Shape " + (shapeValue++).toString()
      }
      else {
        objectType = "image"
        objectValue = "Image " + (imageValue++).toString()
      }
      const objectCoordinates = {
        tl: {
          x: objects[i].getCoords()[0].x,
          y: objects[i].getCoords()[0].y
        },
        tr: {
          x: objects[i].getCoords()[1].x,
          y: objects[i].getCoords()[1].y
        },
        br: {
          x: objects[i].getCoords()[2].x,
          y: objects[i].getCoords()[2].y
        },
        bl: {
          x: objects[i].getCoords()[3].x,
          y: objects[i].getCoords()[3].y
        }
      }
      let objectid = objectId++
      objects[i].name = objectid.toString()

      const element: Element = {
        type: objectType,
        value: objectValue,
        klass: objects[i],
        coordinates: objectCoordinates,
        id: objectid,
        colors: [objects[i].fill as string],
        locked: false,
        selected: false,
        recommendations: [],
        selectedRecommendation: -1,
        plattee: [],
        base64Image: objects[i].toDataURL({ format: "png" })
      }

      elements.forEach((previous_element: any) => {
        if(previous_element.id == element.id){
          element.locked = previous_element.locked
        }
      })

      newElements.push(element);
    }
    console.log(newElements)
    return newElements
  }

  const convertObjectsToElements = () => {
    const updatedElements = getUpdatedElements()
    if (updatedElements !== elements) setElements(updatedElements);
  }

  const handleColorsChange = (colors: string[]): void => {
    setMainColors(colors);
  }

  const handleElementsChange = (element: Element, index: number): void => {
    console.log("element change")
    const newElements: Element[] = [...elements];
    for (let i = 0; i < newElements.length; i++) {
      if (i !== index) {
        newElements[i].selected = false;
      }
    }
    newElements[index] = element;
    setSelected(index);
    setElements(newElements);

    const objects = editor?.canvas.getObjects();
    if (!objects) return 
    objects.forEach( (object) => {
      if (parseInt(object.name as string) == element.id) {
        editor?.canvas.setActiveObject(object);
      }
    })
  }

  const handleRecommendation = (mainColors: string[], elements: Element[]): void => {
    const updatedElements = getUpdatedElements()

    console.log("updated elements")
    console.log(updatedElements)
    console.log("call recommendation rest api")

    let original_images_data = []
    let shapes_data = []
    let text_data = []

    for (let i = 0; i < updatedElements.length; i++) {
      let cur: any = {}
      cur['id'] = updatedElements[i].id
      cur['coordinates'] = updatedElements[i].coordinates
      cur['base64Image'] = updatedElements[i].base64Image
      cur['locked'] = updatedElements[i].locked
      if (updatedElements[i].type == "text") {
        text_data.push(cur)
      }
      else if (updatedElements[i].type == "image") {
        original_images_data.push(cur)
      }
      else {
        shapes_data.push(cur)
      }
    }

    let reqBody = {
      canvas_width: editor?.canvas.getWidth(),
      canvas_height: editor?.canvas.getHeight(),
      theme: mainColors,
      background: ["#ffffff"], // for now
      original_images: original_images_data,
      shapes: shapes_data,
      texts: text_data,
      theme_level: themeEffectValue,
      colorQuantity: colorQuantityValue
    }
    setLoading(true)
    getColorizerRecommendations(reqBody).then((res) => {
      const resData = res.data
      console.log(resData)
      setLoading(false)
      reconstructCanvas(resData, updatedElements)
    });
  }

  const handlePaletteSync = () => {
    let req: any = {}
    const img = editor?.canvas.toDataURL({ format: "jpeg" })
    elements.forEach((element) => {
      if (element.id == 0) {
        req['coordinates'] = element.coordinates
      }
    })
    req['image'] = img
    req['colorQuantity'] = colorQuantityValue

    setLoading(true)
    get2DPlatteeGeneration(req).then((res) => {
      const resData = res.data
      const base64pre = "data:image/png;base64,"
      let base64 = resData['palette']
      setLoading(false)
      setoverviewPalette(base64pre + base64)
    })
  }

  const handleRecommendationsSelectChange = (i: number) => {
    const objects = editor?.canvas.getObjects();
    if (!objects) return

    objects.forEach((object: any) => {
      if (parseInt(object.name as string) == elements[selected]['id']) {
        if (elements[selected].type == "image") {         
          (object as fabric.Image).setSrc(elements[selected].plattee[i], () => {
            const width = object.width as number;
            const height = object.height as number;
            object.set({
              left: elements[selected]['coordinates'].tl.x,
              top: elements[selected]['coordinates'].tl.y,
              scaleX: (elements[selected]['coordinates']['br']['x'] - elements[selected]['coordinates']['bl']['x']) / width,
              scaleY: (elements[selected]['coordinates']['br']['y'] - elements[selected]['coordinates']['tl']['y']) / height
            })
            object.setCoords();
            editor?.canvas.requestRenderAll();
          })
          
        }
        else {
          object.set("fill", elements[selected].recommendations[i], () => {
            editor?.canvas.requestRenderAll();
          })

          elements[selected].colors = [elements[selected].recommendations[i]]
        }
      }
    })
  }


  const reconstructCanvas = (input: any, elements: Element[]): void => {
    const objects = editor?.canvas.getObjects();
    const base64pre = "data:image/png;base64,"
    if (!objects) return

    // console.log(input)
    input['image_palettes'].forEach((image: any) => {
      // console.log(typeof (image['recolored_image']))
      if (typeof (image['recolored_image']) != "string") {
        let base64 = image['recolored_image'][0]
        objects.forEach((object: any) => {
          if (parseInt(object.name as string) == image['id']) {
            (object as fabric.Image).setSrc(base64pre + base64, () => {
              const width = object.width as number;
              const height = object.height as number;
              object.set({
                left: image['coordinates'].tl.x,
                top: image['coordinates'].tl.y,
                scaleX: (image['coordinates']['br']['x'] - image['coordinates']['bl']['x']) / width,
                scaleY: (image['coordinates']['br']['y'] - image['coordinates']['tl']['y']) / height
              })
              object.setCoords();
              editor?.canvas.requestRenderAll();
            })
          }
        })
        elements.forEach((element: Element) => {
          // console.log(image['id'])
          if (image['id'] == element['id']) {
            let recommendation = image['palettes'].map((palette: string) => {
              return base64pre + palette
            })
            let realImage = image['recolored_image'].map((palette: string) => {
              return base64pre + palette
            })
            element.recommendations = recommendation
            element.plattee = realImage
          }
        })
      }
    })

    if (input['shapes']) {
      input['shapes'].forEach((shape: any) => {
        if (!objects) return
        objects.forEach((object: any) => {
          if (parseInt(object.name as string) == shape['id']) {
            object.set("fill", shape['colors'][0], () => {
              editor?.canvas.requestRenderAll();
            })
          }
        })

        elements.forEach((element: Element) => {
          if (shape['id'] == element['id']) {
            element.recommendations = shape['colors']
            element.colors = [shape['colors'][0]]
          }
        })
      })
    }

    if (input['texts']) {
      input['texts'].forEach((text: any) => {
        if (!objects) return
        objects.forEach((object: any) => {
          if (parseInt(object.name as string) == text['id']) {
            object.set("fill", text['colors'][0], () => {
              editor?.canvas.requestRenderAll();
            })
          }
        })

        elements.forEach((element: Element) => {
          if (text['id'] == element['id']) {
            element.recommendations = text['colors']
            element.colors = [text['colors'][0]]

            console.log(element)
          }
        })
      })
    }


    // console.log(elements)
    setElements(elements)
  }

  // editor?.canvas.on("object:added", (options) => {
  //   console.log("object added");
  //   convertObjectsToElements();
  // });

  const add = () => {
    console.log("object added");
    convertObjectsToElements();
  }

  editor?.canvas.on("object:removed", (options) => {
    console.log("object removed");
    convertObjectsToElements();
  });

  // editor?.canvas.on("object:modified", (options) => {
  //   console.log("object modified");
  // const objects = editor?.canvas.getObjects();
  // console.log(objects)
  // });

  editor?.canvas.on("selection:created", (options) => {
    const selected = editor?.canvas.getActiveObject();
    const element = elements.find(el => el.klass === selected);
    console.log("selected", selected);
    //console.log("selected elemented", element);
    // The code below changes a selected object to the colour red. Need to bind the selected object to our elements list, and then 
    // choose the right colour to fill (instead of red)
    if (element) {
      setSelected(0);
    }
    if (element?.type !== "image" && element) {
      const recommendation = element.recommendations[element?.selectedRecommendation];
      if (typeof recommendation === 'string') {
        console.log("recommended colour", recommendation)
        selected.set('fill', recommendation);
      }
    }
  });



  return (
    <div className="App">
      {/* <Navbar bg="dark" variant="dark">
        <NavbarBrand style={{fontSize: 30, padding: '5 0', marginLeft: 15}}>
          Ads Colorizer
        </NavbarBrand>  
      </Navbar> */}

      <ThemeProvider theme={responsiveFontSizes(theme)}>

        <Grid container>
          <Grid container xs={9} >
            <DrawingSettingPanel load={load} add={add} selectedObjects={selectedObjects} editor={editor} onReady={onReady} />
          </Grid>

          <Grid container xs={3} height="100vh" sx={{ backgroundColor: "white", paddingLeft: "20px" }}>
            <Grid item width="100%">
              <ColorSetupSection colors={mainColors} handleColorsChange={handleColorsChange} />
            </Grid>
            <Grid item width="100%">
              <DiscreteSliders
                themeEffectValue={themeEffectValue}
                colorQuantityValue={colorQuantityValue}
                onThemeEffectChange={(val: number) => { setThemeEffectValue(val) }}
                onColorQuantityChange={(val: number) => { setColorQuantityValue(val) }} />
            </Grid>
            <Grid item width="100%">
              <OverviewSection loading={loading} overviewPalette={overviewPalette} handleRecommend={() => { handleRecommendation(mainColors, elements) }} onPaletteSync={() => { handlePaletteSync() }} />
            </Grid>
            <Grid item width="100%">
              <RecommendationsSection handleSelect={(i: number) => {
                if (i === -1) return;
                elements[selected].selectedRecommendation = i;
                handleRecommendationsSelectChange(i)
                setElements([...elements])
              }}
                recommendations={elements[selected]?.recommendations}
                selectedRecommendation={elements[selected]?.selectedRecommendation}
                type={elements[selected] ? elements[selected].type : ""}
              />
            </Grid>
            <Grid item width="100%" height="100%">
              <ControlPanelElementsList elements={elements} handleElementChange={(element: any, index: any) => { handleElementsChange(element, index) }} />
            </Grid>
          </Grid>
        </Grid>
      </ThemeProvider>

    </div >
  );
}

export default App;
