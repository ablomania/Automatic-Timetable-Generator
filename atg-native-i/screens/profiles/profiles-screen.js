import { useNavigation } from "@react-navigation/native";
import { Touchable, TouchableOpacity, Text, StyleSheet, Button, View } from "react-native"

const ProfileScreen = () => {
    const navigation = useNavigation()
    return(
        <View>
            <Text>profiles screen</Text>
            <Button
                title="some profile"
                onPress={() => navigation.navigate('Profile', {profileId: 1})}
            />
        </View>
    );
}

const styles = StyleSheet.create({
    card: {
        borderWidth: 1,
        borderColor: '#c5c5c5',
        borderRadius: 10,
        marginVertical:5,
        padding:30,
    }
})

export default ProfileScreen;