import { Box, Collapse, Fade, IconButton } from "@mui/material"
import AddIcon from '@mui/icons-material/Add';
import { SketchPicker } from 'react-color';
import RemoveCircleIcon from '@mui/icons-material/RemoveCircle';

interface ColorPickerProps {
    color: string;
    open: boolean;
    removable?: boolean;
    width: string;
    handleColorSelect: Function;
    handleOpenColorPicker: Function;
    handleColorRemove: Function;
    popupLocation?: {top: string; left: string}
}

export const ColorPicker = (props: ColorPickerProps): React.ReactElement => {
    const { color, open, width, removable, handleColorSelect, handleOpenColorPicker, handleColorRemove, popupLocation } = props;

    const onColorSelect = (color: any, event: any): void => {
        console.log(color.hex);
        handleColorSelect(color.hex);
    }

    return(
        <Box 
            sx={{
                position:"relative",
                width: "50px",
            }}
        >
            <IconButton
                onClick={() => {handleOpenColorPicker(open)}}
                sx={{
                    backgroundColor: color === "" ? "" : color,
                    color: color === "" ? "#CFCFCF" : "",
                    border: color === "" ? "4px dashed #CFCFCF" : "1px solid grey", 
                    borderRadius: "50%",
                    width: width,
                    height: width,
                    "&:hover": {
                        backgroundColor: color === "" ? "" : color
                    }
                }}
            >
                { color === "" ? <AddIcon fontSize="large"/> : null
                }
            </IconButton>
            <Fade in={color !== "" && removable}>
                <IconButton
                    onClick={() => {handleColorRemove()}}
                    sx={{
                        color: "grey",
                        position: "absolute",
                        right: "-5px",
                        top: "-13px"
                    }}
                >
                    <RemoveCircleIcon />
                </IconButton>
            </Fade>
            
            <Box sx={{
                position: "absolute",
                zIndex: 999999,
                left: `${popupLocation ? popupLocation.left : "-100px"}`, 
                top: `${popupLocation ? popupLocation.top : "25px" }`
            }}>
                <Collapse in={open} sx={{ zIndex: 99999}}>
                    <SketchPicker color={color} 
                        onChangeComplete={onColorSelect}
                    />
                </Collapse>
            </Box>
            
        </Box>
    )
}