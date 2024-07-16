import { createStackNavigator } from '@react-navigation/stack';
import HomeScreen from '../screens/home';
import DetailScreen from '../screens/details';
import { navOptions } from './options';
import { useNavigation } from '@react-navigation/native';
import ProfileScreen from '../screens/profiles/profiles-screen';
import ProfileDetailScreen from '../screens/profiles/profile-detail';
import HomeTabs from './tabs';

const Stack = createStackNavigator();

export const HomeStack = () => {
  const navigation = useNavigation()
  return (
    <Stack.Navigator
    screenOptions={()=> navOptions(navigation)}>
      <Stack.Screen name="HomeTabs"
        options={{
          title: "Home"
        }}
        component={HomeTabs} 
       />
      <Stack.Screen name="Details" component={DetailScreen} />
    </Stack.Navigator>
  );
}



export const ProfileStack = () => {
  const navigation = useNavigation()
  return (
    <Stack.Navigator
      screenOptions={()=> navOptions(navigation)}>
      <Stack.Screen name="Profiles" component={ProfileScreen} />
      <Stack.Screen name="Profile" component={ProfileDetailScreen} />
    </Stack.Navigator>
  );
}