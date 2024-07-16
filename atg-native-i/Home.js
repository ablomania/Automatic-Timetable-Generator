import React from "react";
import { View, Text, Button, StatusBar,StyleSheet,FlatList } from "react-native";

const data = new Array(10).fill(500).map(
    (v, i) => ({ key: i.toString(), value:`Item ${i}`})
);

export default function Home() {
    return (
        <View>
            <FlatList 
            data={data}
            renderItem={({ item }) => <Text>{item.value}</Text>} />
        </View>
    )
}
const styles = StyleSheet.create({
    container: {
        justifyContent: "center",
        alignItems: "center",
    }
})