import { Grid, IconButton } from "@mui/material";
import { ColorPicker } from "./ColorPicker";
import { ControlPanelSectionHeader } from "./ControlPanelSectionHeader";
import { Palette2D } from "./Palette2D";


interface RecommendationSectionProps {
    recommendations?: string[];
    selectedRecommendation: number;
    handleSelect: Function;
    type: string;
}


const RecommendationsSection = (props: RecommendationSectionProps): React.ReactElement => {
    const { recommendations, selectedRecommendation, handleSelect, type } = props;

    return (
        <Grid
            width="100%"
            sx={{
                paddingTop: "10px",
                borderBottom: "1px solid #000000"
            }}
            container
            direction="column"
            justifyContent="center"
        >
            <Grid item>
                <ControlPanelSectionHeader>
                    Recommendations
                </ControlPanelSectionHeader>
            </Grid>
            <Grid
                item
                container
                direction="column"
                justifyContent="flex-start"
                alignItems="flex-start"
                height={"90px"}
                overflow="scroll"
            >
                {
                    recommendations && recommendations.length > 0 ? recommendations.map((r, i) => {
                        if (Array.isArray(r)) {
                            return (
                                <Grid item key={i} marginRight="20px"
                                    onClick={() => { handleSelect(i) }}
                                    sx={{
                                        border: i === selectedRecommendation ? "2px solid #000000" : "none",
                                    }}
                                >
                                    {type === "image" ?
                                        <img src={`${r}`} />
                                        : <Palette2D colors={r} width="75px" />
                                    }
                                </Grid>
                            )
                        } else {
                            if (type === "image") {
                                return (
                                    <Grid item key={i} marginRight="20px"
                                        onClick={() => { handleSelect(i) }}
                                        sx={{
                                            border: i === selectedRecommendation ? "2px solid #000000" : "none",
                                        }}
                                    >
                                        <img src={`${r}`} width="75px" />
                                    </Grid>
                                )
                            }

                            else {
                                return (
                                    <Grid item key={i}
                                        marginRight="20px"
                                        onClick={() => { handleSelect(i) }}
                                        sx={{
                                            paddingRight: "30px",
                                            border: i === selectedRecommendation ? "2px solid #000000" : "none"
                                        }}
                                    >
                                        <ColorPicker
                                            color={r}
                                            open={false}
                                            removable={false}
                                            handleColorSelect={() => { }}
                                            handleColorRemove={() => { }}
                                            handleOpenColorPicker={() => { }}
                                            width="80px"
                                        />
                                    </Grid>
                                )
                            }
                        }
                    })
                        : "No Recommendations"}
            </Grid>
        </Grid>
    )
}

export default RecommendationsSection;