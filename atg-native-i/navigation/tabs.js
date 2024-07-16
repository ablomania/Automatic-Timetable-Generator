import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import HomeScreen from '../screens/home';
import QrCodeScreen from '../screens/qr-code';
import { Ionicons } from '@expo/vector-icons';

const Tab = createBottomTabNavigator();

export default function HomeTabs() {
  return (
    <Tab.Navigator 
        screenOptions={({ route }) => ({
            headerShown:false,
            tabBarShowLabel: false,
            tabBarStyle: {
                backgroundColor: 'black',
            },
            tabBarActiveTintColor: "yellow",
            tabBarInactiveTintColor: "grey",
            tabBarIcon: ({focused, color, size}) => {
                let iconName;
                if(route.name === 'Home') {
                    iconName = focused ? 'home': 'home-outline';
                }
                else if(route.name === 'QrCode') {
                    iconName = focused ? 'qr-code': 'qr-code-outline';
                }

                return <Ionicons name={iconName} size={focused ? 35: size} color={color} />
            }
            })}>
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="QrCode" component={QrCodeScreen} />
    </Tab.Navigator>
  );
}