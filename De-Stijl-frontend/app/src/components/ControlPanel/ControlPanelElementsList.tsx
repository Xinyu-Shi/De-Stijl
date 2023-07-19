import { Grid } from '@mui/material';
import React, { useState } from 'react';
import { ControlPanelSectionHeader } from './ControlPanelSectionHeader';
import ElementItem from './ElementItem';


interface ControlPanelElementsListProps {
    elements: any[];
    handleElementChange: Function;
}

const ControlPanelElementsList = (props: ControlPanelElementsListProps): React.ReactElement => {
    const { elements, handleElementChange } = props;
    const [ openedPicker, setOpenedPicker ] = useState<number>(-1);

    return (
        <Grid 
            width="100%"
            minHeight="100%"
            height="100%"
            paddingTop="10px"
            direction="row"
            justifyContent="flex-start"
            alignItems="flex-start"
        >
            <ControlPanelSectionHeader>
                Objects
            </ControlPanelSectionHeader>
            <Grid
                direction="row"
                justifyContent="flex-start"
                alignItems="flex-start"
                sx={{
                    overflowY:'scroll',
                    height:"40%"
                }}
            >
                {
                    elements.map((element, i) => {
                        return <ElementItem
                            key={i}
                            element={element}
                            index={i}
                            pickerOpen={i === openedPicker}
                            handleColorOpen={()=>{
                                    if (i === openedPicker) {
                                        setOpenedPicker(-1);
                                    } else {
                                        setOpenedPicker(i);
                                    }
                                }
                            }
                            handleElementChange={handleElementChange}
                        />
                    })
                }
            </Grid>
        </Grid>
    )

}

export default ControlPanelElementsList;