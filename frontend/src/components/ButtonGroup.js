import { useEffect, useState } from 'react';

const ButtonGroup = ({ buttons, label , allowMultiple = false, onChange, defaultValue = allowMultiple ? [] : null, value, className}) => {

    const [selectedValue, setSelectedValue] = useState(value ? value : defaultValue);

    const removeFromValue = (value) => {
        let newSelectedValue = selectedValue;

        if (allowMultiple) {
            const indexOfValue = newSelectedValue.indexOf(value);
            newSelectedValue.splice(indexOfValue, 1);

            setSelectedValue(newSelectedValue);
            onChange(newSelectedValue);
        } 
    }

    const addToValue = (value) => {
        setSelectedValue(allowMultiple ? [...selectedValue, value] : value);
        onChange(allowMultiple ? [...selectedValue, value] : value);
    }

    useEffect(() => {
        if (value !== undefined) setSelectedValue(value);
    }, [value])

    return (
        <div className={`${className} button-group`} title={label}>
            { label && <p className="group-label" >{ label }</p>}

            { buttons.map(button => (
                <label 
                    key={button.value}
                    className={(allowMultiple ? selectedValue.includes(button.value) : selectedValue === button.value && 'active') || ''}>
                    <input 
                        type="checkbox" 
                        value={button.value} 
                        name={label} 
                        checked={ allowMultiple ? selectedValue.includes(button.value) : selectedValue === button.value }
                        onChange={(e) => {

                            if (e.target.checked) addToValue(e.target.value);
                            else  removeFromValue(e.target.value);

                        }} /> {button.label}
                </label>
            ))}
        </div>
    )
}

export default ButtonGroup;