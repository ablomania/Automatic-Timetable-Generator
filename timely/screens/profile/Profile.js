import AsyncStorage from "@react-native-async-storage/async-storage";
import { useEffect, useState } from "react"
import { View, Text, StyleSheet, Button, ScrollView } from "react-native";



export default function Profile({navigation}) {
    const [ userName, setUserName ] = useState("");
    const [ departmentName, setDepartmentName ] = useState("");
    const [ yearGroup, setYearGroup ] = useState("")
    const [ collegeName, setCollegeName ] = useState("");
    const [ tableCode, setTableCode ] = useState("");

    useEffect(()=> {
        getDetails();
    },[])
    async function getDetails() {
        try{
            const storedUserName = await AsyncStorage.getItem("userName");
            // const storedDepartmentName = await AsyncStorage.getItem("");
            const storedyearGroup = await AsyncStorage.getItem("yearGroup");
            const storedCollegeName = await AsyncStorage.getItem("collegeName");
            const storedtableCode = await AsyncStorage.getItem("tableCode");
            setUserName(storedUserName);
            setYearGroup(storedyearGroup);
            // setDepartmentName(storedDepartmentName);
            setCollegeName(storedCollegeName);
            setTableCode(storedtableCode);
        } catch(error) {
            console.log("Could not get stored details")
        }
    }
    return(
        <ScrollView>
            <View style={styles.container}>
                <View style={styles.item}>
                    <Text style={styles.label}>Name:</Text>
                    <Text style={styles.value}>{userName}</Text>
                </View>
                <View style={styles.item}>
                    <Text style={styles.label}>Department:</Text>
                    <Text style={styles.value}>{departmentName}</Text>
                </View>
                <View style={styles.item}>
                    <Text style={styles.label}>Year Group:</Text>
                    <Text style={styles.value}>{yearGroup}</Text>
                </View>
                <View style={styles.item}>
                    <Text style={styles.label}>College:</Text>
                    <Text style={styles.value}>{collegeName}</Text>
                </View>
                <View style={styles.item}>
                    <Text style={styles.label}>Table code:</Text>
                    <Text style={styles.value}>{tableCode}</Text>
                </View>
                <Button title="Edit" onPress={() => navigation.navigate("EditProfile")} />
            </View>
        </ScrollView>
    )
}

const styles = StyleSheet.create({
    container: {
      padding: 16,
      backgroundColor: '#fff',
    },
    label: {
      fontSize: 16,
      fontWeight: 'bold',
      marginBottom: 4,
    },
    value: {
      fontSize: 16,
      color: '#333',
      marginBottom: 12,
    },
    item: {
        backgroundColor: '#fafafa',
        borderRadius: 10,
        padding: 10,
        marginVertical: 10,
    }
  });