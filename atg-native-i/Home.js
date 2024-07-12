import React from "react";
import { View, Text, Button, StatusBar,StyleSheet,FlatList } from "react-native";

const data = new Array(100).fill(null).map(
    (v, i) => ({ key: i.toString(), value:`Item ${i}`})
);

export default function Home() {
    return (
        <View>
            <FlatList 
            data={data}
            renderItem={({ item }) => <Text>{item.value}</Text>} />
            {/* <Text>Home Content</Text> */}
            {/* <StatusBar barStyle="dark-content" />
            <Text>Home Screen</Text>
            <Button title="Settings"
            onPress={() => navigation.navigate("Settings")}
            />
            <Button title="First Item"
            onPress={() => navigation.navigate("Details", { title: "First Item" })}
             />
            <Button title="Second Item"
            onPress={() => navigation.navigate("Details", { title: "Second Item" })}
             />
            <Button title="Third Item"
            onPress={() => navigation.navigate("Details", { title: "Third Item" })}
             /> */}
        </View>
    )
}
const styles = StyleSheet.create({
    container: {
        justifyContent: "center",
        alignItems: "center",
    }
})