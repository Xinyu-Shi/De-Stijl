import { Box, Grid, Slider, Typography } from "@mui/material";
import { ControlPanelSectionHeader } from "./ControlPanelSectionHeader";

interface DiscreteSliderProps {
    themeEffectValue: number;
    colorQuantityValue: number;
    onThemeEffectChange: Function;
    onColorQuantityChange: Function;
}

export const DiscreteSliders = (props: DiscreteSliderProps): React.ReactElement => {
    const { themeEffectValue, colorQuantityValue, onThemeEffectChange, onColorQuantityChange } = props;
    const colorSliderMarks = [
        { value: 1, label: "Less"},
        { value: 2, label: "Normal"},
        { value: 3, label: "More"}
    ]

    const handleThemeSlider = (event: Event, value: number | number[], activeThumb: number): void => {
        if (event !== null) {
            onThemeEffectChange(value);
        }
    }

    const handleColorSlider = (event: Event, value: number | number[], activeThumb: number): void => {
        if (event !== null) {
            onColorQuantityChange(value);
        }
    }
    return (
        <Grid paddingTop="10px">
            <Box>
                <Typography variant="body2" component="p">
                    Theme Effect
                </Typography>
            </Box>
            <Box paddingLeft="20px" paddingRight="20px">
                <Slider
                    value={themeEffectValue}
                    step={2}
                    min={2}
                    max={10}
                    marks
                    onChange={handleThemeSlider}
                />
            </Box>
             <Box>
                <Typography variant="body2" component="p">
                    Color Quantity
                </Typography>
            </Box>
            <Box paddingLeft="20px" paddingRight="20px">
                <Slider
                    value={colorQuantityValue}
                    step={1}
                    marks={colorSliderMarks}
                    min={1}
                    max={3}
                    onChange={handleColorSlider}
                />
            </Box>
        </Grid>
    )
}