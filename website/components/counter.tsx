import React, {useState} from "react";

interface IProps {
    target: number;
    callback?: () => any;
}

export const Counter: React.FunctionComponent<IProps> = (props) => {
    const [current, setCurrent] = useState<number>(0);

    const target = Math.round(props.target);
    const increment = props.target < 0 ? -1 : 1;

    if (target !== current) {
        // Update current value to be closer to target.
        // Delay is increased as current value approaches target.
        const proximity = Math.pow(1 - Math.abs(target - current) / 100, 4);
        setTimeout(() => setCurrent(current + increment), 200 * proximity);
    } else {
        if (props.callback) {
            props.callback();
        }
    }

    return <span>{current}</span>;
};
