//
// Imports
//

#include "basic_colors.inc"
#include "hc_colors.inc"

//
// Syntax
//
// Syntax highlighting in editors and input boxes

ParmSyntaxPlainColor: #bcbec3
ParmSyntaxStringColor: #79a978
ParmSyntaxVarColor: #c892ca
ParmSyntaxFuncColor: #8888c1
ParmSyntaxKeywordColor: #6799c0
ParmSyntaxQuoteColor: #c59172
ParmSyntaxNumberColor: #ebb845
ParmSyntaxRefColor: #d2cf9c
ParmSyntaxCommentColor: #7b7e84
ParmSyntaxErrorColor: #e14640
ParmSyntaxTypeColor: #93d4eb
ParmSyntaxExtraColor: #8b588a

ParmParenMatchColor: #FFB41F // Gold
ParmQuoteMatchColor: #FFB41F // Gold
ParmMisMatchColor: #E14640 // Red

PreEditUnderlineColor: SELECTION_BASE
TextboxLineNumberFG: text
TextboxLineNumberBG: DRKBASE
TextboxLineNumberHighlight: DRKGRADHIGH

//
// Parameters
//

ButtonColor: DRKGRADHIGH
ButtonStripColor: UNK
SliderColor: GREY(0.65)
SliderThumbColor: GREY(0.68)
InputColor: GREY(0.70)
RadioColor: GREY(0.60)

//
// Scene graph panes
//

UsdLocationHasArcs: #3E9E2E
UsdLocationIsInstance: #87CEFA
UsdLocationInPrototype: #7688D9
UsdLocationUnloaded: #5E2E15
UsdLocationLoaded: #DE9E2E
UsdLayerMuted: #9090E0
UsdLayerHasOpinion: #E07000
UsdLayerChildHasOpinion: #A04000
UsdLayerModifiedByCurrentLop: #40A000

UsdAttrResolveFallback: #DE9E2E
UsdAttrResolveDefault: #87CEFA
UsdAttrResolveValueClips: #E696E6
UsdAttrResolveTimeSamples: #B1CF99
UsdAttrResolveNone: grey50
UsdRelationship: #E68484
UsdComputed: #8484E6

UsdPrimSelected: SELECTION_BASE
UsdPrimSelectedAlpha: 0.4
UsdChildPrimSelected: 0.44 0.22 0.11
UsdChildPrimSelectedAlpha: 0.4
UsdPrimModified: 0.30 0.80 0.80
UsdPrimModifiedAlpha: 0.4
UsdChildPrimModified: 0.15 0.40 0.40
UsdChildPrimModifiedAlpha: 0.4

//
// Network editor: node flags
//

SelectOnColor: 0.75 0.75 0
SelectOffColor: 0.56 0.56 0
DisplayOnColor: 0.3 0.5 1
DisplayOffColor: 0.2 0.3 0.6
TemplateOnColor: 1 0.5 1
TemplateOffColor: 0.75 0.37 0.75
BypassOnColor: 1 0.5 0
BypassOffColor: 0.5 0.25 0
SelectableOnColor: 0.6 0.35 0.2
SelectableOffColor: 0.4 0.2  0.15
ExposeOnColor: 1 0 0
ExposeOffColor: 0.6 0 0
CurrentColor: 0.25 0.85 0.25

//
// Statusbar
//

MessageColor: 0.0 0.0 0.0
PromptColor: 0.3 0.4 0.9
WarningColor: 0.85 0.25 0.0
ErrorColor: error

//
// Network editor
//

NodeConnectionDefaultBG: GREY(0.5)
NodeConnectionTextBG: 0.415 0.395 0.44
NodeConnectionGlow: HSV 40 0.5 1
NodeConnectionArrowLight: black
NodeConnectionArrowDark: black
NodeConnectionBevel: GREY(0.6)
NodeConnectionTopBorder: GREY(0.2)
NodeConnectionBottomBorder: GREY(0.2)

NodeButtonGrad: GREY(0.5)
NodeButtonSelectedGrad: UNK // NodeButtonSelectedGrad does not seem to be used anymore
NodeButtonBevel: GREY(0.55)
NodeButtonBevelSelected: UNK
NodeSeparator: GREY(0.2)
NodeSeparatorEnabled: GREY(0.33)
NodeError: error
NodeWarningBG: black
NodeWarningFG: 1.0 0.87 0
NodeDefaultBG: DRKBASE
NodeHighlight: 0 0.68 0.94
NodeDebugFG: 0.741 0.988 1

NodeTemplateFlag: #FF66FF
NodeSelectableTemplateFlag: #CC33CC
NodeBypassFlag: 1.0 1.0 0
NodeRenderFlag: 0.666 0.5 1.0
NodeDisplayFlag: 0 0.4 0.8
NodeDisplayAndRenderFlag: 0 0.68 0.94
NodeOutputFlag: 0.75 0.4 0.0
NodeSelectableFlag: 0.4 0.8 0
NodeExportFlag: 0.75 0.4 0.0
NodeHiddenFlag: 0.58 0.55 0.43
NodeAudioFlag: 0.0 0.5 0.5
NodeThumbnailFlag: 0.35 0.6 0.2
NodeLockFlag: #FF3300
NodeSoftLockFlag: #C4E361
NodeLoadedWithUnloadFlagOn: 1.0 0.0 1.0
NodeDebugFlag: 0.741 0.988 1

NetworkSelection: HSV 65 1 0.95
NetworkCurrent: HSV 45 1 0.95
NetworkCurrentNonSelected: GREY(1.0)
NetworkBackground: DRKBASE
NetworkDisplayHighlight: 0.257 0.396 0.521
NetworkRenderHighlight: 0.375 0.310 0.498
NetworkOutputHighlight: 0.75 0.4 0.0
NetworkTemplateHighlight: #FF66FF
NetworkLegacyHighlight: #FF3333
NetworkOverviewDragger: white
NetworkTimeDependent: 0.0 1.0 0.0

NetworkGrid: GREY(0.29)

NetworkWireNormal: GREY(.55)
NetworkWireActive: HSV 45 0.6 0.55
NetworkWireActiveLight: HSV 45 0.65 0.8
NetworkWireHighlight: 1.0 1.0 0.0
NetworkWireShadow: black
NetworkWireExtraNormal: HSV 160 0.6 0.55
NetworkWireExtraActive: HSV 0 0.6 0.55
NetworkWireExtraActiveLight: HSV 0 0.65 0.8
NetworkWireIKNormal: HSV 240 0.6 0.55
NetworkWireIKActive: HSV 240 0.6 0.55
NetworkWireIKActiveLight: HSV 240 0.65 0.8
NetworkWireOutputOverrideNormal: 1.0 1.0 1.0
NetworkWireOutputOverrideHighlight: 1.0 0.784 0.0
NetworkWireTimeDepNormal: 0.0 1.0 0.0
NetworkWireLoopBack: HSV 180 1.0 1.0 1.0
NetworkWirePassThrough: HSV 180 1.0 1.0 1.0

//
// SHOP viewer
//

ShopViewTitleColor 1.0 1.0 0.0

//
// VOP input/output labels
//

VopInOutVectorColor: #60C279
VopInOutVectorArrayColor: #448C69
VopInOutVector2Color: #27FF00
VopInOutVector2ArrayColor: #178902
VopInOutVector4Color: #C6FF00
VopInOutVector4ArrayColor: #6F8F00
VopInOutNormalColor: #A4A4FF
VopInOutColorColor: #FF24FF
VopInOutFloatColor: #55D2C5
VopInOutFloatArrayColor: #218278
VopInOutIntColor: #45B5FF
VopInOutIntArrayColor: #21668A
VopInOutStringColor: #CCB299
VopInOutStringArrayColor: #A97442
VopInOutMatrix2Color: #D367FF
VopInOutMatrix2ArrayColor: #783A91
VopInOutMatrix3Color: #B367FF
VopInOutMatrix3ArrayColor: #6A488C
VopInOutMatrix4Color: #7F68FE
VopInOutMatrix4ArrayColor: #5B5195
VopInOutPointColor: #EF99D5
VopInOutBsdfColor: #F8E71C
VopInOutStructColor: #DE796E
VopInOutStructArrayColor: #A45858
VopInOutMethodColor: #FF9900
VopInOutMultiColor: #E5E5E5
VopErrorColor: error
VopInOutDictColor: #D29628
VopInOutDictArrayColor: #B5700A

//
// COP input/output labels
//

CopInOutIntColor: #99DDFF
CopInOutFloatColor: #77AADD
CopInOutVector2Color: #EE8866
CopInOutVectorColor: #44BB99
CopInOutVector4Color: #BBCC33
CopInOutGeometryColor: #FFAABB
CopInOutMetadataColor: #DDDDDD
CopInOutUndefColor: #FFFFFF

//
// SHOP input/output labels
//

ShopInOutSurfaceColor: #e5b299
ShopInOutShadowColor: #33334c
ShopInOutDisplaceColor: #99b2e5
ShopInOutGeometryColor: #b2e5b2
ShopInOutLightColor: #e5e599
ShopInOutFogColor: #b2b2b2
ShopInOutPropertiesColor: #7fcce5
ShopInOutShaderColor: #e5e5e5
ShopInOutImage3dColor: #66e5b2
ShopInOutImage3dArrayColor: #4cb299

//
// DOP input/output labels
//

DopInOutObjectColor: #a5a5a5
DopInOutDataColor: #7fcc7f
DopInOutRelDataColor: #339933
DopInOutSolverColor: #b27fe5
DopInOutAnyColor: #e5e5e5

//
// TOP graph nodes
//

TopInOutColor_file: #919191
TopInOutColor_file/image: #55D2C5
TopInOutColor_file/geo: #008FEE
TopInOutColor_file/csv: #FF6600
TopInOutColor_file/movie: #5AAA00
TopInOutColor_file/archive: #BEC43F
TopInOutColor_nonfile: #D05ADD
