import Box from '@material-ui/core/Box';
import withStyles from "@material-ui/core/styles/withStyles";

export const ButtonGroupBox = withStyles((theme) => ({
    root: {
        backgroundColor: 'transparent',
        color: theme.palette.common.white,
        boxShadow: 'none',
        display: 'flex',
        alignItems: 'center',
        flexWrap: 'wrap',
        borderBottom: `1px solid ${theme.palette.common.white}`,
        borderRadius: '0px',
        padding: theme.spacing(0.5),

        "& .MuiFormLabel-root": {
            color: theme.palette.common.white
        },

        "& .MuiToggleButtonGroup-root": {
            padding: `${theme.spacing(0.5)}px`
        }
    }
}))(Box)