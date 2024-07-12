import React from "react";
import { View, Text, Button, StatusBar } from "react-native";

export default function Settings() {
    return(
        <View>
            <StatusBar barStyle="dark-content" />
            <Text>Settings Screen</Text>
            {/* <Button title="Home" onPress={() => navigation.navigate("Home")} /> */}
        </View>
    )
}