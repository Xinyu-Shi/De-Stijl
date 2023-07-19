import { Box, Grid, Typography } from "@mui/material"

interface ControlPanelSectionHeaderProps {
    children: any;
}
export const ControlPanelSectionHeader = (props: ControlPanelSectionHeaderProps): React.ReactElement => {
    const { children } = props;
    return (
        <Grid item xs={12}>
            <Box>
                <Typography variant="body2" component="div" >
                    <b> { children } </b>
                </Typography>
            </Box>
        </Grid>
    )
}