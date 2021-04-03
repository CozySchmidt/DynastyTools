import withStyles from "@material-ui/core/styles/withStyles";
import ToggleButtonGroup from '@material-ui/lab/ToggleButtonGroup'

export const CustomToggleButtonGroup = withStyles((theme) => ({
    root: {
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'flex-start',
        width: '100%'
    }
}))(ToggleButtonGroup)