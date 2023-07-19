import { Button, Grid, IconButton } from "@mui/material";
import { ControlPanelSectionHeader } from "./ControlPanelSectionHeader";
import { Palette2D } from "./Palette2D";
import SyncIcon from '@mui/icons-material/Sync';
import { Tooltip } from "react-bootstrap";
import LoadingButton from '@mui/lab/LoadingButton';

interface OverviewSectionsProps {
    handleRecommend: Function;
    overviewPalette?: string;
    onPaletteSync: Function;
    loading: boolean
}

const OverviewSection = (props: OverviewSectionsProps): React.ReactElement => {
    const { handleRecommend, overviewPalette, onPaletteSync, loading } = props;
    return (
        <Grid
            container
            direction="row"
            justifyContent="space-between"
            alignItems="center"
            sx={{
                paddingTop: "10px",
                paddingBottom: "10px",
                borderBottom: "1px solid #000000"
            }}
        >
            <Grid item paddingBottom="5px">
                {/* <Palette2D colors={overviewPalette || []} width="75px" /> */}

                <Grid item>
                    <img src={`${overviewPalette}`} width="100px" />
                </Grid>

                {
                    loading ?
                        <LoadingButton
                            disabled
                            loading={loading}
                            sx={{
                                position: "absolute",
                                marginTop: "-20px",
                                marginLeft: "50px"
                            }}
                        >
                            <SyncIcon />
                        </LoadingButton> :

                        <IconButton onClick={() => { onPaletteSync() }} sx={{
                            position: "absolute",
                            marginTop: "-20px",
                            marginLeft: "50px"
                        }}>
                            <SyncIcon />
                        </IconButton>
                }

            </Grid>

            <Grid item width="70%">
                {
                    loading ?
                        <LoadingButton
                            variant="contained"
                            disabled
                            loading={loading}
                            sx={{
                                borderRadius: "10px",
                                color: "#000000",
                                width: "95%"
                            }}
                        >
                            Recommend
                        </LoadingButton>
                        :
                        <Button
                            variant="outlined"
                            sx={{
                                borderRadius: "10px",
                                color: "#000000",
                                width: "95%"
                            }}
                            onClick={() => { handleRecommend() }}
                        >
                            Recommend
                        </Button>
                }
            </Grid>
        </Grid>
    )

}

export default OverviewSection;