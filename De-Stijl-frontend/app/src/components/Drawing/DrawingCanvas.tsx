import { Grid, Button } from '@mui/material';
import ButtonGroup from '@mui/material/ButtonGroup';
import TextFieldsOutlinedIcon from '@mui/icons-material/TextFieldsOutlined';
import ImageOutlinedIcon from '@mui/icons-material/ImageOutlined';
import DeleteOutlineOutlinedIcon from '@mui/icons-material/DeleteOutlineOutlined';
import DeleteSweepOutlinedIcon from '@mui/icons-material/DeleteSweepOutlined';
import SquareOutlinedIcon from '@mui/icons-material/SquareOutlined';
import CircleOutlinedIcon from '@mui/icons-material/CircleOutlined';
import FormatShapesOutlinedIcon from '@mui/icons-material/FormatShapesOutlined';
import SaveAltOutlinedIcon from '@mui/icons-material/SaveAltOutlined';
import DownloadForOfflineOutlinedIcon from '@mui/icons-material/DownloadForOfflineOutlined';

import ChangeHistoryOutlinedIcon from '@mui/icons-material/ChangeHistoryOutlined';
import CategoryOutlinedIcon from '@mui/icons-material/CategoryOutlined';

import React, { MutableRefObject, useEffect, useRef } from 'react';
import { fabric } from "fabric";
import { FabricJSCanvas, FabricJSEditor, useFabricJSEditor } from 'fabricjs-react'


interface DrawingSettingPanelProps {
  selectedObjects?: fabric.Object[];
  editor?: FabricJSEditor;
  onReady: (f: fabric.Canvas) => void;
  add: () => void;
  load: () => void;
}

const DrawingSettingPanel = (props: DrawingSettingPanelProps): React.ReactElement => {
  const { selectedObjects, editor, onReady, add, load} = props;
  const [text, setText] = React.useState("");

  const inputFile = useRef() as MutableRefObject<HTMLInputElement>;
  const inputShape = useRef() as MutableRefObject<HTMLInputElement>;

  let canvasWidth = 900
  let canvasHeight = 700
  editor?.canvas.setHeight(canvasHeight);
  editor?.canvas.setWidth(canvasWidth);

  // const resizeCanvas = (canvas: any) => {
  //   let canvas_temp = document.getElementById("canvas") as HTMLElement
  //   canvasWidth = canvas_temp.getBoundingClientRect().width
  //   canvasheight = canvas_temp.getBoundingClientRect().height
  //   canvas.setDimensions({
  //     width: canvasWidth,
  //     height: canvasheight
  //   })
  //   canvas.renderAll();
  // }
  // resizeCanvas(editor?.canvas)
  // console.log(canvasWidth)
  // console.log(canvasheight)
  // window.addEventListener("resize", resizeCanvas( editor?.canvas as fabric.Canvas ), false)

  // const add = () => {
  //   console.log("add")
  // }

  const onAddCircle = () => {
    const circle = new fabric.Circle({
      strokeUniform: true,
      radius: 25,
      stroke: "white",
      fill: "white"
    });
    editor?.canvas.add(circle);
    editor?.canvas.requestRenderAll();
    add()
  }

  const onAddRectangle = () => {
    const rectangle = new fabric.Rect({
      width: 50,
      height: 50,
      stroke: "white",
      fill: "white"
    });
    editor?.canvas.add(rectangle);
    editor?.canvas.requestRenderAll();
    add()
  }

  const onDeleteSelected = () => {
    editor?.deleteSelected();
  }

  const onAddText = () => {
    // if (selectedObjects?.length) {
    //   return editor?.updateText(text)
    // }
    const object = new fabric.Textbox(text, {
      type: 'text',
      left: 100,
      top: 100,
      fontSize: 16,
      fontFamily: 'Arial',
      fill: '#000000'
    })
    object.set({ text: "text" })
    editor?.canvas.add(object);
    editor?.canvas.requestRenderAll();
    add()
  }

  const upload = (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const target = event.target as HTMLInputElement;
    const file: File = (target.files as FileList)[0];

    var fileType = file.type;
    var url = URL.createObjectURL(file)

    // if (fileType === 'image/jpg' || fileType === 'image/png' || fileType === 'image/jpeg') {
    fabric.Image.fromURL(url, function (img) {
      img.scaleToWidth(180);
      img.scaleToHeight(180);
      editor?.canvas.add(img);
      editor?.canvas.requestRenderAll();
      add()
    });

  
    // }

    // if (fileType === 'image/svg+xml') {
    //   });
    // }
  }

  const uploadShape = (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const target = event.target as HTMLInputElement;
    const file: File = (target.files as FileList)[0];

    var fileType = "path";
    if (file.name.substring(0, 4) == "text") {
      fileType = "text"
    }
    var url = URL.createObjectURL(file)
    fabric.loadSVGFromURL(url, function (objects, options) {
      var svg = fabric.util.groupSVGElements(objects, options);
      svg.set({
        left: canvasWidth / 4,
        top: canvasHeight / 4,
        type: fileType
      })
      svg.scaleToWidth(100);
      svg.scaleToHeight(100);
      editor?.canvas.add(svg);
      editor?.canvas.requestRenderAll();
      add()
    })    
  }

  const onDeleteAll = () => {
    editor?.deleteAll();
  }

  const save = () => {
    const dataURL =  editor?.canvas.toDataURL({
      width: editor?.canvas.width,
      height: editor?.canvas.height,
      left: 0,
      top: 0,
      format: 'png',
    }) as string
    const link = document.createElement('a');
    link.download = 'image.png';
    link.href = dataURL;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  // const load = () => {
  //   console.log("load")
  // }

  const buttons = [
    <Button key="load" sx={{ color: "black" }} onClick={load}>
    <DownloadForOfflineOutlinedIcon />
  </Button>,

    <Button key="circle" sx={{ color: "black" }} onClick={onAddCircle}>
      <CircleOutlinedIcon />
    </Button>,

    /** <Button key="triangle" sx={{color: "black"}} onClick={onAddR}>
      <ChangeHistoryOutlinedIcon />
    </Button>, **/

    <Button key="rect" sx={{ color: "black" }} onClick={onAddRectangle}>
      <SquareOutlinedIcon />
    </Button>,
    <Button key="text" sx={{ color: "black" }} onClick={onAddText}>
      <TextFieldsOutlinedIcon />
    </Button>,
    <Button key="shape" sx={{ color: "black" }} onClick={() => { inputShape.current.click() }}>
      <FormatShapesOutlinedIcon />
    </Button>,
    <Button key="image" sx={{ color: "black" }} onClick={() => { inputFile.current.click() }}>
      <ImageOutlinedIcon />
    </Button>,
    <Button key="delete" sx={{ color: "black" }} onClick={onDeleteSelected}>
      <DeleteOutlineOutlinedIcon />
    </Button>,
    <Button key="clear" sx={{ color: "black" }} onClick={onDeleteAll}>
      <DeleteSweepOutlinedIcon />
    </Button>,
    <Button key="save" sx={{ color: "black" }} onClick={save}>
      <SaveAltOutlinedIcon />
    </Button>
  ]

  return (
    <Grid container
      direction="row"
      justifyContent="flex-start"
      alignItems="center"
    >
      <input type='file' id='file' ref={inputFile} style={{ display: 'none' }} onChange={(e) => upload(e)} />
      <input type='file' id='file' ref={inputShape} style={{ display: 'none' }} onChange={(e) => uploadShape(e)} />
      <ButtonGroup
        orientation="vertical"
        aria-label="vertical outlined button group"
        variant="text"
        size="large"
        sx={{
          backgroundColor: "white",
          border: "none"
        }}
      >
        {buttons}
      </ButtonGroup>
      <Grid id="canvas-warpper">
        <FabricJSCanvas className="canvas" onReady={onReady} />
      </Grid>
    </Grid>
  )
}

export default DrawingSettingPanel;