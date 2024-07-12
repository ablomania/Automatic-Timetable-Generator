import React from "react";
import { View, Text, StatusBar } from "react-native";

export default function ({route, navigation}) {
    const { content, title } = route.params;

    React.useLayoutEffect(() => {
        navigation.setOptions({ title });
    }, [])
    return(
        <View>
            <StatusBar barStyle="dark-content" />
            <Text>{content}</Text>
        </View>
    )
}