import { Fade, Grid } from "@mui/material";
import { useState } from "react";
import { ColorPicker } from "./ColorPicker";
import { ControlPanelSectionHeader } from "./ControlPanelSectionHeader";

interface ColorSetupSectionProps {
    /** Currently selected colors */
    colors: string[]
    /** Callback function to update new list of colors */
    handleColorsChange: Function;
}

/**
 * Returns the section of the control panel that allows users to select, remove,
 *  and edit their brand/theme colours.
 * @param props 
 */
const ColorSetupSection = (props: ColorSetupSectionProps): React.ReactElement => {
    const { colors, handleColorsChange } = props;
    const [ openedColor, setOpenedColor ] = useState<number>(-1);
    
    const handleColorSelect = (color: string, index: number): void => {
        const newColors: string[] = [...colors];
        newColors[index] = color;
        handleColorsChange(newColors);
    }

    const handleColorRemove = (index: number): void => {
        const newColors: string[] = [...colors];
        newColors.splice(index, 1);
        handleColorsChange(newColors);
    }


    return (
        <Grid
            container
            direction="row"
            justifyContent="flex-start"
            alignItems="center"
            spacing={2}
            sx={{
                paddingTop:"10px",
                paddingBottom: "10px",
                borderBottom: "1px solid #000000"
            }}
        >
            <ControlPanelSectionHeader>
                Theme Colors
            </ControlPanelSectionHeader>
           
            {
                colors.slice(0, 5).map((color, i) => {
                    return(
                        <Grid item key={i}> 
                            <ColorPicker 
                                color={color} 
                                removable={true}
                                width="35px"
                                handleColorSelect={(newColor: string) => {
                                    handleColorSelect(newColor, i);
                                }}
                                open={openedColor === i}
                                handleOpenColorPicker={() => {
                                    setOpenedColor(i === openedColor ? -1 : i)
                                }}
                                handleColorRemove={() => {handleColorRemove(i)}}
                            />
                        </Grid>
                    )
                })
            }
            <Fade in={colors.length < 5}>
                <Grid item>
                    <ColorPicker 
                        width="35px"
                        color=""
                        handleColorSelect={(newColor: string, index: number) => {
                            handleColorSelect(newColor, colors.length);
                            setOpenedColor(-1);
                        }}
                        open={openedColor === colors.length}
                        handleOpenColorPicker={() => {
                            setOpenedColor(colors.length === openedColor ? -1 : colors.length)
                        }}
                        handleColorRemove={() => {}}
                    />
                </Grid>
            </Fade>

        </Grid>
    )
}

export default ColorSetupSection;