import ToggleButton from '@material-ui/lab/ToggleButton';
import withStyles from "@material-ui/core/styles/withStyles";
import { darken } from '@material-ui/core/styles';

export const CustomToggleButton = withStyles((theme) =>  ({
    root: {
        backgroundColor: theme.palette.primary.dark,
        color: theme.palette.common.white,
        border: 'none',
        padding: `${theme.spacing(0.5)}px ${theme.spacing(1)}px`,
        margin: theme.spacing(0.5),
        "&&.Mui-selected": {
            backgroundColor: theme.palette.secondary.dark,
            color: theme.palette.common.white,
            boxShadow: `0 0 8px ${theme.palette.secondary.main}`
        },
        "&&.Mui-selected + &.Mui-selected": {
            marginLeft: theme.spacing(0.5),
            borderLeft: '1px solid transparent'
        },
        "&&:hover": {
            backgroundColor: darken(theme.palette.secondary.dark, 0.15),
            color: theme.palette.common.white,
            boxShadow: `0 0 8px ${theme.palette.secondary.dark}`
        },
        '&&.MuiToggleButtonGroup-groupedHorizontal:not(:first-child)': {
            borderRadius: theme.shape.borderRadius,
            marginLeft: theme.spacing(0.5)
        },
        '&&.MuiToggleButtonGroup-groupedHorizontal:first-child': {
            borderRadius: theme.shape.borderRadius
        }
    },
    
}))(ToggleButton);