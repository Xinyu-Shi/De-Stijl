import { Box, Collapse, Grid, IconButton, Typography } from "@mui/material";
import { Element } from "../../App";

import ImageIcon from '@mui/icons-material/Image';
import TextFieldsIcon from '@mui/icons-material/TextFields';
import CategoryOutlinedIcon from '@mui/icons-material/CategoryOutlined';
import QuestionMarkIcon from '@mui/icons-material/QuestionMark';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import LockOpenOutlinedIcon from '@mui/icons-material/LockOpenOutlined';

import { ColorPicker } from "./ColorPicker";
import { Palette2D } from "./Palette2D";
import { useEffect, useState } from "react";
import { ChromePicker, SketchPicker } from "react-color";

interface ElementItemProps {
    element: Element;
    index: number;
    handleElementChange: Function;
    handleColorOpen: Function;
    pickerOpen: boolean;
}

const ElementItem = (props: ElementItemProps): React.ReactElement => {
    const { element, index, handleElementChange, handleColorOpen, pickerOpen } = props;
    const [color, setColor] = useState<string>(element.colors[0]);

    useEffect(() => {
        if (element.colors[0] !== color) {
            onElementChange("color", color);
        }
    }, [color]);


    const onElementChange = (type: string, value?: any): void => {
        const newElement: Element = element;
        if (type === "select") {
            newElement.selected = true;
        } else if (type === "lock") {
            newElement.locked = !newElement.locked;
        } else if (type === "color") {
            newElement.recommendations.unshift(value);
            newElement.selectedRecommendation = 0;
        }
        handleElementChange(newElement, index);
    }

    const getIcon = (type: string): React.ReactElement => {
        if (type === "image") {
            return <ImageIcon />
        } else if (type === "text") {
            return <TextFieldsIcon />
        } else if (type === "shape") {
            return <CategoryOutlinedIcon />
        } else {
            return <QuestionMarkIcon />
        }
    }

    const getPreview = (element: Element): React.ReactElement => {
        const type = element.type;
        const value = element.value;

        if (type === "text" || type === "shape") {
            const imgWidth = element.klass.width;
            const imgHeight = element.klass.height;
            if (imgWidth > imgHeight) {
                console.log("landscape");
                return (
                    <Box margin={2}>
                        <img src={element.base64Image} width={50} height="auto" style={{
                            filter: "grayscale(1)",
                        }}/>
                    </Box>
                )
            } else {
                return  (
                    <Box margin={2}>
                        <img src={element.base64Image} height={50} width="auto" style={{
                            filter: "grayscale(1)",
                        }}/>
                    </Box>
                )
            }
            
        } else {
            return (
                 <Box margin={2}>
                    <img src={element.base64Image} height={50}/>
                </Box>
             )
        }
    }

    const getColor = (type: string, colors: string[]): React.ReactElement => {
        if (type === "text" || type === "shape") {
            return (
                <ColorPicker
                    color={color}
                    open={pickerOpen}
                    removable={false}
                    width="50px"
                    handleColorSelect={(newColor: string) => { setColor(newColor) }}
                    handleColorRemove={() => { }}
                    handleOpenColorPicker={handleColorOpen}
                    popupLocation={{ top: "0px", left: "-200px" }}
                />
            )
        } else {
            return (
                <Palette2D colors={colors} width="50px" />
            )
        }
    }

    const getLock = (): React.ReactElement => {
        if (element.locked) {
            return (
                <IconButton onClick={() => { onElementChange("lock") }}>
                    <LockOutlinedIcon />
                </IconButton>
            )
        } else {
            return (
                <IconButton onClick={() => { onElementChange("lock") }}>
                    <LockOpenOutlinedIcon />
                </IconButton>
            )
        }
    }



    return (
        <Grid
            container
            direction="row"
            justifyContent="space-between"
            alignItems="center"
            sx={{
                border: element.selected ? '2px solid #EAEBED' : '2px solid transparent',
                borderRadius: element.selected ? '10px' : 'none',
                borderBottom: '1px solid rgba(0, 0, 0, 0.1)',
                boxSizing: 'border-box',
                padding: "5px"
            }}
            onClick={() => { onElementChange("select") }}
        >
            <Grid
                container
                direction="row"
                justifyContent="flex-start"
                alignItems="center"
                width="50%"
            >
                <Grid item>
                    {getIcon(element.type)}
                </Grid>
                <Grid item>
                    {getPreview(element)}
                </Grid>
            </Grid>
            <Grid
                item
                container
                direction="row"
                justifyContent="flex-end"
                alignItems="center"

                width="50%"
            >
                <Grid item>
                    {getColor(element.type, element.colors)}
                </Grid>
                <Grid item>
                    {getLock()}
                </Grid>
            </Grid>

        </Grid>
    )
}

export default ElementItem;