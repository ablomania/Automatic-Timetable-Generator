import { useRoute, useNavigation } from "@react-navigation/native";
import { useLayoutEffect } from "react";
import { StyleSheet, View, Text } from "react-native";
import { HeaderBackButton } from "@react-navigation/elements";


const DetailScreen = () => {
    const route = useRoute()
    const navigation = useNavigation()

    const {eventId, title, description} = route.params

    useLayoutEffect(() => {
        navigation.setOptions({
            headerTitle: "new title",
            headerLeft:() => (
                <HeaderBackButton 
                tintColor = "white"
                onPress = {() => navigation.goBack()}
                />
            )
        },[])
    })
    return(
        <View style={styles.screen}>
            <Text style={{fontSize:20}}>This is the details screen for {eventId}</Text>
            <Text>{title}</Text>
            <Text>{description}</Text>
        </View>
    );
}

const styles = StyleSheet.create({
    screen: {
        padding: 20,
    }
})

export default DetailScreen;