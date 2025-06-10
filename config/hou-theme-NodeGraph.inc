#include "NodeGraphCommon.inc"
#include "hou-theme-colors.inc"


////////////////////////
// Wires & Connectors //
////////////////////////


GraphConnector:                     #605000            // connector
GraphConnectorLabel:                GREY(0.70)         // connector label
GraphConnectorError:                #CE5E5E            // connector error
GraphWire:                          #a09000            // wire
GraphWireUnused:                    0.40 0.40 0.40     // wire unused
GraphWireError:                     red                // wire error
GraphWireLoopBack:                  0.30 0.30 1.00     // wire loopback
GraphWireSelection:                 #ffbb00            // wire selection
GraphWireNodeSelection:             yellow             // wire node selection
GraphWireLongFaded:                 0.50 0.50 0.50     // wire long faded
GraphWireLongerFaded:               0.50 0.50 0.50     // wire longer faded
GraphWireStub:                      GREY(0.70)         // wire stub
GraphWireStubSelection:             yellow             // wire stub selection
GraphWireCut:                       red                // wire cut
GraphWireCutPath:                   0.95 0.30 0.00     // wire cut path
GraphWireStitchStart:               #B8E986            // wire stitch start
GraphWireStitchEnd:                 #B8E986            // wire stitch end
GraphSpareWire:                     #8967D9            // wire spare
GraphParmOverrideWire:              #FFA500            // wire parm override
GraphDependency:                    #9A6955            // dependency
GraphDependencyEndAffector:         #668E4A            // dependency
GraphDependencyExternalIn:          GREY(0.8)          // dependency
GraphDependencyExternalOut:         GREY(0.8)          // dependency


///////////////
// Selection //
///////////////


GraphPickFill:                      #aa9000            // drag selection bg
GraphPreSelection:                  0.75 0.86 1.0      // item pre selection
GraphItemCurrent:                   node_current       // item current
GraphItemSelectionContrast:         node_current       // item selection contrast
GraphItemCurrentNonSelected:        #b0b0b0            // item current non-selected
GraphItemSelection:                 #b0b0b0            // multi-selection
GraphItemContentsSelection:         red                // item selection contents
GraphSnapLine:                      #5C704D            // item snap line
GraphDotPinAccent:                  GREY(0.3)          // dot accent


/////////////
// General //
/////////////


GraphBackground:                    #000000            // bg
GraphPromptText:                    #404040
GraphGridLines:                     #606020            // grid lines
GraphGridPoints:                    #806020            // grid points
GraphNameText:                      #a0a0a0            // node label
GraphNodeTypeText:                  grey7              // node type text
GraphCommentText:                   grey7              // node comment
GraphDescriptiveNameText:           grey7              // node description?
GraphContextOptionDepsText:         #6DB4BD
GraphOutputForViewText:             #6DB4BD
GraphDetailIdText:                  grey7
GraphNetworkBoxText:                white              // network box text
GraphNetworkBoxTextDark:            black              // network box text dark
GraphNetworkBoxNameText:            #76A8E1            // network box
GraphIndirectText:                  white
GraphIndirectTextDark:              black
GraphItemBorder:                    green
GraphMinimizeButton:                GREY(0.8)


//////////////
// Palettes //
//////////////


PaletteBackground:                  lite               // palette bg
PaletteSelected:                    yellow             // palette selected
ShapePaletteShape:                  grey7              // palette shape
GraphOverviewBackground:            GREY(0.10)         // overview bg
GraphOverviewViewRegion:            0.5 0.3 0.5        // overview region
GraphOverviewBorder:                black              // overview border


//////////////
// BG Image //
//////////////


BackgroundImageLocate:              white
BackgroundImageBorder:              yellow
BackgroundImageBrightness:          yellow
BackgroundImageLink:                GREY(0.8)


//////////////////
// Overlay Text //
//////////////////


GraphOverlayLeftText:               0.2 0.9 0.9
GraphOverlayCenterText:             #a0a0a0
GraphOverlayRightText:              #a0a0a0


///////////
// Flags //
///////////


GraphTemplateFlag:                  node_flag          // flag template
GraphSelectableTemplateFlag:        node_flag          // flag selectable template
GraphBypassFlag:                    node_flag          // flag bypass
GraphRenderFlag:                    node_flag          // flag render
GraphDisplayFlag:                   node_flag          // flag display
GraphOutputFlag:                    node_flag          // flag output
GraphSelectableFlag:                node_flag          // flag selectable
GraphExportFlag:                    node_flag          // flag export
GraphHiddenFlag:                    #90BECD            // flag hidden
GraphAudioFlag:                     0.00 0.50 0.50     // flag audio
GraphThumbnailFlag:                 0.35 0.60 0.20     // flag thumbnail
GraphLockFlag:                      #FF 33 00          // flag lock
GraphSoftLockFlag:                  #C4 E3 61          // flag softlock
GraphDebugFlag:                     #6CC6B2            // flag debug
GraphMaterialFlag:                  0.75 0.40 0.00     // flag material
GraphDisplayAndRenderFlag:          node_flag          // flag display and render
GraphDisplayAndOutputFlag:          node_flag          // flag display and output
GraphFilterFlag:                    #55FFC1            // flag filter
GraphDisplayHighlight:              node_circle        // circle hilite display
GraphExportHighlight:               node_circle        // circle hilite export
GraphRenderHighlight:               node_circle        // circle hilite render
GraphOutputHighlight:               node_circle        // circle hilite output
GraphTemplateHighlight:             node_circle        // circle hilite template
GraphFilterHighlight:               node_circle        // circle hilite filder


////////////
// Subnet //
////////////


GraphSubnetShadow1:                 mud                // subnet shadow1
GraphSubnetShadowBlend1:            0.9                // subnet shadow1 blend
GraphSubnetShadow2:                 mud                // subnet shadow2
GraphSubnetShadowBlend2:            0.9                // subnet shadow2 blend


////////////
// Flyout //
////////////


GraphFlyoutBackgroundFlagOn:        black              // flyout
GraphFlyoutBackgroundFlagOff:       black              // flyout
GraphFlyoutEdgeFlagOff:             GREY(0.3)          // flyout
GraphFlyoutInfo:                    GREY(0.1)          // flyout
GraphFlyoutWarning:                 0.2 0.2 0.0        // flyout
GraphFlyoutError:                   0.2 0.0 0.0        // flyout


////////////
// Badges //
////////////


GraphErrorBadgeDot:                 red                // badge error
GraphChildErrorBadgeDot:            1.00 0.00 0.00     // badge child error
GraphWarningBadgeDot:               0.77 0.60 0.04     // badge warning
GraphMessageBadgeDot:               0.05 0.45 1.00     // badge message
GraphCommentBadgeDot:               0.15 0.67 0.64     // badge comment
GraphNodeLockedBadgeDot:            1.00 0.35 0.43     // badge locked
GraphNodeUnloadBadgeDot:            0.60 0.65 0.73     // badge unload
GraphNodeHasDataBadgeDot:           0.45 0.75 0.45     // badge has data
GraphNeedsCookBadgeDot:             0.97 0.91 0.11     // badge needs cook
GraphHdaLockedBadgeDot:             0.43 0.47 0.48     // badge hda locked
GraphHdaUnlockedBadgeDot:           0.98 0.49 0.55     // badge hda unlocked
GraphHdaDelaySyncBadgeDot:          0.70 0.70 0.70     // badge hda delay sync
GraphTimeDependentBadgeDot:         0.72 0.91 0.53     // badge time dependent
GraphVexCachedBadgeDot:             #FF5AD2            // badge cached vex
GraphVexCachableBadgeDot:           #AA3E8C            // badge cachable vex
GraphNotCompilableBadgeDot:         #E5B985            // badge not compilable
GraphConstraintsBadgeDot:           #97C473            // badge constraints
GraphKinematicsBadgeDot:            #FF9370            // badge kinematics
GraphHasTakeDataBadgeDot:           #979797            // badge has take data
GraphNodeUnloadBadgeDot:            #D19F9F            // badge node unload
GraphNodeHasDataBadgeDot:           #9FABD1            // badge has data
Graph64bitBadgeDot:                 #AC68CC            // badge 64 bit
GraphPdgDynamicBadgeDot:            #E5C8FF            // badge pdg dynamic
GraphUnloadedPayloadsBadgeDot:      #EDC486            // badge unloaded payloads
GraphPopulationMaskBadgeDot:        #A06B9A            // badge population mask
GraphDiveableBadgeDot:              #73d216            // badge diveable
GraphLoadFromDiskBadgeDot:          #dceefaff          // badge load from disk


//////////////////////
// Network Contexts //
//////////////////////

// COP

GraphCopMaskInput:                  0.50 0.80 0.50     // COP mask input
GraphCopPreviewBackground:          GREY(0.1)          // COP preview bg
GraphCopBottomButtonEnabled:        GREY(0.1)          // COP

// DOP

GraphDopObjectData:                 0.65 0.65 0.65     // DOP object data
GraphDopData:                       0.50 0.80 0.50     // DOP data
GraphDopRelData:                    0.20 0.60 0.20     // DOP rel data
GraphDopSolverData:                 0.70 0.50 0.90     // DOP solver data
GraphDopAnyData:                    0.90 0.90 0.90     // DOP any data

// LOP

GraphLopLayerOutline:               GREY(0.6)          // LOP layer outline
GraphLopLayerColor1:                0.30 0.70 0.20     // LOP layer color 1
GraphLopLayerColor2:                0.60 0.40 0.20     // LOP layer color 2
GraphLopLayerColor3:                0.90 0.10 0.20     // LOP layer color 3
GraphLopLayerColor4:                0.30 0.20 0.30     // LOP layer color 4
GraphLopLayerColor5:                0.60 0.20 0.60     // LOP layer color 5
GraphLopLayerColor6:                0.90 0.20 0.90     // LOP layer color 6
GraphLopLayerColor7:                0.20 0.70 0.30     // LOP layer color 7
GraphLopLayerColor8:                0.20 0.40 0.60     // LOP layer color 8
GraphLopLayerColor9:                0.20 0.10 0.90     // LOP layer color 9
GraphLopLastModifiedPrimText:       #6DB4BD
GraphLopLayerCountText:             #6DB4BD

// SHOP

GraphShopConnectorBackground:       GREY(0.1)          // SHOP connector bg

// SOP

GraphSopHeightfield:                #25aa8e            // SOP heightfield
GraphSopConstraints:                #D879D8            // SOP constraint
GraphSopDomain:                     #6bcae2            // SOP domain
GraphSopRestGeometry:               0.58 0.77 1.0      // SOP rest geo
GraphSopCapturePose:                0.60 0.60 0.60     // SOP capture pose
GraphSopAnimatedPose:               1.00 0.72 0.00     // SOP anim pose

// TOP

GraphPdgProgressOutline:            white              // PDG progress outline
GraphPdgProgressPrecook:            #324D59            // PDG progress precook
GraphPdgProgressCooking:            #B8E986            // PDG progress cooking
GraphPdgProgressCooked:             #4D623F            // PDG progress cooked
GraphPdgProgressWarning:            #EBF802            // PDG progress warning
GraphPdgProgressError:              #FF3300            // PDG progress error
GraphPdgProgressIncomplete:         #75876A            // PDG progress incomplete
GraphPdgProgressErrorCircle:        #D0021B            // PDG progress error circle
GraphPdgProgressErrorFill:          #730000            // PDG progress error fill
GraphPdgProgressNormalFill:         #232323            // PDG progress normal fill
GraphPdgSummaryBackground:          GREY(0.18)         // PDG summary bg
GraphPdgSummaryFilterOn:            FFD42A             // PDG summary filter on
GraphPdgSummaryWorkItemCooked:      #73945D            // PDG summary work item cooked
GraphPdgSummaryWorkItemCooking:     #B8E986            // PDG summary work item cooking
GraphPdgSummaryWorkItemWaiting:     #879889            // PDG summary work item waiting
GraphPdgSummaryWorkItemUncooked:    GREY(0.5)          // PDG summary work item uncooked
GraphPdgSummaryWorkItemFailed:      #EE5A6C            // PDG summary work item failed
GraphPdgSummaryWorkItemCancelled:   #EBB502            // PDG summary work item cancelled
GraphTaskGraphBackground:           GREY(0.1)          // task graph bg
GraphTaskGraphBorder:               GREY(0.7)          // task graph border
GraphTaskGraphSeeMore:              GREY(0.9)          // task graph see more
GraphTaskGraphWorkItemCooked:       #529232            // task graph work item cooked
GraphTaskGraphWorkItemCached:       #529232            // task graph work item cached
GraphTaskGraphWorkItemCooking:      #ADFF49            // task graph work item cooking
GraphTaskGraphWorkItemWaiting:      #354B60            // task graph work item waiting
GraphTaskGraphWorkItemUncooked:     GREY(0.5)          // task graph work item uncooked
GraphTaskGraphWorkItemFailed:       #FF3300            // task graph work item failed
GraphTaskGraphWorkItemCancelled:    #69511B            // task graph work item cancelled
GraphTaskGraphWorkItemSelected:     #FFD42A            // task graph work item selected
GraphTaskGraphWorkItemHovered:      #33EEFF            // task graph work item hovered
GraphTaskGraphWorkItemAncestor:     #99FF79            // task graph work item ancestor
GraphTaskGraphWorkItemDescendant:   #2AFFCB            // task graph work item descendant
GraphTaskGraphNormalWire:           GREY(0.9)          // task graph wire normal
GraphTaskGraphMappedWire:           #80FFA2            // task graph wire mapped
GraphTaskGraphIndirectWire:         #D9DD70            // task graph wire indirect
GraphTaskGraphWorkItemPerfFast:     #009166            // task graph work item performance fast
GraphTaskGraphWorkItemPerfMed:      #f6ff00            // task graph work item performance med
GraphTaskGraphWorkItemPerfSlow:     #ff9000            // task graph work item performance slow
GraphTaskGraphWorkItemPerfNA:       GREY(0.35)         // task graph work item performance NA
GraphTaskGraphStatusBarFailed:      #FF9C9C            // task graph status bar failed
GraphTaskGraphStatusBarCancelled:   #F7DF1B            // task graph satus bar cancelled
GraphTaskGraphStatusBarCooked:      #529232            // task graph status bar cooked
GraphTaskGraphStatusBarCooking:     #B7DF86            // task graph status bar cooking
GraphTaskGraphStatusBarWaiting:     GREY(0.6)          // task graph status bar waiting
GraphTaskGraphStatusBarEmpty:       GREY(0.2)          // task graph status bar empty
GraphTaskGraphLogError:             #D04548            // task graph log error
GraphTaskGraphLogWarning:           #B8B834            // task graph log warning
GraphTaskPageRect:                  #D8D8D8
GraphTopBottomButtonEnabled:        GREY(0.1)
GraphTopBottomButtonDisabled:       GREY(0.6BADGES)

// VOP

GraphVopConnectorGroupName:         white              // VOP
GraphVopConnectorBackground:        grey4              // VOP node bg
GraphVopBottomButtonEnabled:        GREY(0.1)          // VOP
GraphVopBottomButtonDisabled:       GREY(0.6)          // VOP
