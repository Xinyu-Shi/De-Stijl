import { Box, Grid } from "@mui/material";

interface Palette2DProps {
    colors: string[];
    width: string;
}

export const Palette2D = (props: Palette2DProps): React.ReactElement => {
    const { colors, width } = props;
    return (
        <Grid
            container
            direction="row"
            justifyContent="center"
            alignItems="center"
            width={width}
        >
            {
                colors.map((color, i) => {
                    return(
                        <Grid item key={i}>
                            <Box sx={{
                                border: '1px solid black',
                                backgroundColor: color,
                                width: `calc(${width}/3)`,
                                height: `calc(${width}/3)`
                            }}>
                            </Box>
                        </Grid>
                    )
                })
            }
        </Grid>
    )
}