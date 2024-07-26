import AsyncStorage from "@react-native-async-storage/async-storage";
import { useNavigation } from "@react-navigation/native";
import { useEffect, useState } from "react";
import { Touchable, TouchableOpacity, Text, StyleSheet, Button, View } from "react-native"

const ProfileScreen = () => {
    const navigation = useNavigation()
    const [ userName, setUserName] = useState("");
    const [ code, setCode ] = useState("");
    useEffect(() => {
        const getStoredData = async () => {
            try {
                const storedUserName = await AsyncStorage.getItem('userName');
            //   const storedYearGroup = await AsyncStorage.getItem('yearGroup');
            //   const storedCollege = await AsyncStorage.getItem('college');
            //   const storedDepartmentName = await AsyncStorage.getItem('departmentName');
                const storedcode = await AsyncStorage.getItem('code');
                setUserName(storedUserName);
                setCode(storedcode);
            
            } catch (error) {
              console.error('Error retrieving data:', error);
            }
        }
        getStoredData()
    
    }, [])
    
    
    return (
    <View style={styles.container}>
        {/* <Image source={user.profileImage} style={styles.profileImage} /> */}
        <Text style={styles.userName}>{userName}</Text>
        <Text style={styles.code}>{code}</Text>
        {/* Add other user details (e.g., followers, posts, etc.) */}
    </View>
    );
};
    
const styles = StyleSheet.create({
    container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 16,
    },
    profileImage: {
    width: 120,
    height: 120,
    borderRadius: 60,
    marginBottom: 16,
    },
    userName: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 8,
    },
    code: {
    fontSize: 16,
    textAlign: 'center',
    color: '#777',
    },
    // Add styles for other user details (followers, posts, etc.)
});
export default ProfileScreen;