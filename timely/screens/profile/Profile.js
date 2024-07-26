import AsyncStorage from "@react-native-async-storage/async-storage";
import { useEffect, useState } from "react"
import { View, Text, StyleSheet } from "react-native";



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
        <View style={styles.container}>
            <Text style={styles.label}>Name:</Text>
            <Text style={styles.value}>{userName}</Text>
            <Text style={styles.label}>Department:</Text>
            <Text style={styles.value}>{departmentName}</Text>
            <Text style={styles.label}>Year Group:</Text>
            <Text style={styles.value}>{yearGroup}</Text>
            <Text style={styles.label}>College:</Text>
            <Text style={styles.value}>{collegeName}</Text>
            <Text style={styles.label}>Table code:</Text>
            <Text style={styles.value}>{tableCode}</Text>
        </View>
    )
}

const styles = StyleSheet.create({
    container: {
      padding: 16,
      backgroundColor: '#f9f9f9',
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
  });